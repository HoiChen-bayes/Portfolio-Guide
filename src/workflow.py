"""Real, isolated model role calls; deterministic replay never invokes a model."""
from __future__ import annotations
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import tomllib

ROOT = Path(__file__).resolve().parents[1]
ROLES = ('finance', 'research', 'scenario', 'qa')

def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False, separators=(',', ':'))

def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()

def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()

def write(path, value):
    Path(path).write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')

def read(path):
    return json.loads(Path(path).read_text())


def deny_actuals(value):
    if isinstance(value, dict):
        for k, v in value.items():
            if k.lower() in {'actuals', 'target_actuals', 'target_results', 'holdout'}:
                raise ValueError('Target actuals forbidden in forecast packets')
            deny_actuals(v)
    elif isinstance(value, list):
        for v in value: deny_actuals(v)

def validate_packet(packet):
    for key in ('company', 'sector', 'cutoff', 'target_period', 'history', 'evidence', 'driver_contract'):
        if key not in packet:
            raise ValueError(f'Missing packet field: {key}')
    cutoff = dt.date.fromisoformat(packet['cutoff'])
    start = dt.date.fromisoformat(packet['target_period']['start'])
    end = dt.date.fromisoformat(packet['target_period']['end'])
    if start > end or cutoff >= end:
        raise ValueError('Invalid forecast target or cutoff')
    deny_actuals(packet)
    ids = set()
    for kind in ('history', 'evidence'):
        for row in packet[kind]:
            if row.get('excluded_from_model', False):
                raise ValueError('Excluded source cannot enter a model packet')
            pub = dt.date.fromisoformat(row['published_at'][:10])
            if pub > cutoff:
                raise ValueError(f'Post-cutoff source: {row["source_id"]}')
            if kind == 'history' and row.get('period_end') and dt.date.fromisoformat(row['period_end']) >= start:
                raise ValueError('Target-period history forbidden')
            ids.add(row['source_id'])
    drivers = [r['driver'] for r in packet['driver_contract']]
    if len(drivers) != len(set(drivers)):
        raise ValueError('Duplicate driver contract')
    if (packet.get('vintage', '').startswith('history_only') or packet.get('vintage') in {'pre_history', 'mid_history'}) and packet['evidence']:
        raise ValueError('History-only packet contains market evidence')
    canonical(packet)
    return ids

def schema_validate(value, schema, location='output'):
    """Validate the deliberately small strict schema subset, without external packages."""
    typ = schema['type']
    valid = {'object':isinstance(value,dict), 'array':isinstance(value,list),
             'string':isinstance(value,str), 'number':isinstance(value,(int,float)) and not isinstance(value,bool)}[typ]
    if not valid: raise ValueError(f'{location}: expected {typ}')
    if 'enum' in schema and value not in schema['enum']: raise ValueError(f'{location}: invalid enum')
    if typ == 'object':
        if set(value) != set(schema['required']): raise ValueError(f'{location}: incorrect keys')
        for k,v in value.items(): schema_validate(v,schema['properties'][k],location+'.'+k)
    if typ == 'array':
        for i,v in enumerate(value): schema_validate(v,schema['items'],f'{location}[{i}]')
    canonical(value)

def validate_output(role, output, packet):
    schema_validate(output, read(ROOT/'config'/'schemas'/f'{role}.json'))
    if output['role'] != role: raise ValueError('Role mismatch')
    sources = validate_packet(packet)
    for row in output.get('mappings', []) + output.get('signals', []) + output.get('assumptions', []) + output.get('findings', []):
        refs = row.get('source_ids', [row['source_id']] if 'source_id' in row else [])
        if not set(refs) <= sources: raise ValueError('Unknown source citation')
    if role == 'scenario':
        rows = output['assumptions']; contracts = {r['driver']:r for r in packet['driver_contract']}
        if len(rows) != len(contracts) or {r['driver'] for r in rows} != set(contracts):
            raise ValueError('Scenario must cover exactly every driver')
        for row in rows:
            contract = contracts[row['driver']]
            if row['unit'] != contract['unit']: raise ValueError('Driver unit mismatch')
            for case in ('bear','base','bull'):
                if not contract.get('min',float('-inf')) <= row[case] <= contract.get('max',float('inf')):
                    raise ValueError('Driver outside contract bounds')
    if role == 'qa':
        excerpts = all(r.get('source_excerpt') for kind in ('history','evidence') for r in packet[kind]) and bool(packet['history'])
        if not excerpts and (output['source_accuracy'] != 'not_verified' or output['decision'] == 'pass'):
            raise ValueError('QA cannot attest source accuracy without original excerpts')
        if output['decision'] == 'pass' and any(f['severity']=='blocker' for f in output['findings']):
            raise ValueError('QA pass contradicts blocker')

def configured_model():
    """Read only the model choice; never copy credentials or broad user configuration."""
    home = Path(os.environ.get('CODEX_HOME', Path.home()/'.codex'))
    try:
        config = tomllib.loads((home/'config.toml').read_text())
        return config.get('model'), config.get('model_reasoning_effort')
    except FileNotFoundError:
        return None, None

def model_role(role, payload, out_dir, model=None, timeout=900):
    packet = payload.get('packet', payload)
    deny_actuals(payload)
    validate_packet(packet)
    out_dir = Path(out_dir); out_dir.mkdir(parents=True, exist_ok=False)
    write(out_dir/'input.json', payload)
    prompt = (ROOT/'agents'/f'{role}.md').read_text() + '\nINPUT JSON:\n' + canonical(payload)
    (out_dir/'prompt.txt').write_text(prompt)
    inherited, effort = configured_model()
    model = model or inherited
    meta = {'role':role, 'status':'started', 'started_at':now(), 'input_sha256':digest(payload),
            'prompt_sha256':hashlib.sha256(prompt.encode()).hexdigest(),
            'schema_sha256':hashlib.sha256((ROOT/'config'/'schemas'/f'{role}.json').read_bytes()).hexdigest(),
            'requested_model':model or 'CLI default', 'requested_reasoning_effort':effort or 'CLI default',
            'execution':'genuine_codex_exec', 'tool_policy':'disabled', 'retrospective':True}
    write(out_dir/'run.json',meta)
    try:
        with tempfile.TemporaryDirectory(prefix='financial-role-') as tmp:
            schema_path = Path(tmp)/'schema.json'
            shutil.copyfile(ROOT/'config'/'schemas'/f'{role}.json',schema_path)
            final_path=Path(tmp)/'final.json'
            cmd=['codex','exec','--ignore-user-config','--ephemeral','--skip-git-repo-check',
                 '--sandbox','read-only','--cd',tmp,'--json','--color','never',
                 '--output-schema',str(schema_path),'--output-last-message',str(final_path),
                 '-c','approval_policy="never"','-c','web_search="disabled"','-c','project_doc_max_bytes=0',
                 '-c','mcp_servers={}','-c','plugins={}']
            for feature in ('shell_tool','unified_exec','apps','plugins','hooks','browser_use','browser_use_external',
                            'computer_use','in_app_browser','image_generation','view_image','multi_agent','memories',
                            'skill_search','skill_mcp_dependency_install','code_mode_host','workspace_dependencies'):
                cmd += ['--disable',feature]
            if model: cmd += ['--model',model]
            if effort: cmd += ['-c',f'model_reasoning_effort={json.dumps(effort)}']
            cmd += ['-']
            result = subprocess.run(cmd,input=prompt,text=True,capture_output=True,timeout=timeout)
            (out_dir/'events.jsonl').write_text(result.stdout)
            (out_dir/'runtime.stderr.txt').write_text(result.stderr)
            meta['returncode']=result.returncode
            if result.returncode: raise RuntimeError('Codex failed; see runtime.stderr.txt; no model result accepted')
            # Reject any runtime tool use even if a future CLI changes feature defaults.
            for line in result.stdout.splitlines():
                try: event=json.loads(line)
                except json.JSONDecodeError: continue
                if event.get('type') == 'turn.completed': meta['usage'] = event.get('usage', {})
                item=event.get('item',{})
                if item and item.get('type') not in {'agent_message', 'reasoning', 'error'}:
                    raise RuntimeError('Unexpected tool use: role isolation not established')
            output=read(final_path)
            validate_output(role,output,packet)
            write(out_dir/'output.json',output)
            meta.update(status='completed',output_sha256=digest(output))
    except Exception as exc:
        meta.update(status='failed',error=f'{type(exc).__name__}: {exc}')
        raise
    finally:
        meta['finished_at']=now(); write(out_dir/'run.json',meta)
    return output

def run_pipeline(packet_path, run_dir, model=None, timeout=900):
    packet=read(packet_path); validate_packet(packet)
    run_dir=Path(run_dir); run_dir.mkdir(parents=True,exist_ok=False)
    write(run_dir/'packet.json',packet)
    results={}
    for role in ROLES:
        results[role]=model_role(role,{'packet':packet,'prior_outputs':results},run_dir/role,model,timeout)
    if results['qa']['decision'] != 'pass':
        raise RuntimeError('QA did not pass; outputs retained, no freeze written')
    files=['packet.json']
    for role in ROLES: files += [f'{role}/{name}' for name in ('input.json','prompt.txt','output.json','run.json')]
    freeze={'frozen_at':now(),'status':'assumptions_frozen','packet_sha256':digest(packet),
            'files':{f:hashlib.sha256((run_dir/f).read_bytes()).hexdigest() for f in files},
            'disclosure':'Retrospective execution; date-filtered inputs do not erase model pretraining.'}
    write(run_dir/'freeze.json',freeze)
    return freeze

def review_qa(run_dir, supplement_path, model=None, timeout=900):
    """One independent QA re-review with new original-source support; assumptions unchanged."""
    run_dir=Path(run_dir)
    if (run_dir/'freeze.json').exists(): raise ValueError('Already frozen; do not modify accepted run')
    if (run_dir/'qa_initial').exists(): raise ValueError('Initial QA already archived; use a new review run')
    packet=read(run_dir/'packet.json'); validate_packet(packet)
    prior={role:read(run_dir/role/'output.json') for role in ROLES}
    for role in ROLES: validate_output(role,prior[role],packet)
    if prior['qa']['decision']=='pass': raise ValueError('No rejected QA to re-review')
    supplement=read(supplement_path);deny_actuals(supplement)
    if not supplement.get('reviews'): raise ValueError('Supplement must contain dated original-source reviews')
    for source_review in supplement['reviews']:
        if source_review['publication_date'] > packet['cutoff']:
            raise ValueError('Post-cutoff source in QA supplement')
        if source_review['source_id'] not in validate_packet(packet):
            raise ValueError('QA supplement must cite a source already in the packet')
    # Preserve the rejected review and every byte of the three earlier role results.
    (run_dir/'qa').rename(run_dir/'qa_initial')
    write(run_dir/'qa_supplement.json',supplement)
    result=model_role('qa',{'packet':packet,'prior_outputs':{r:prior[r] for r in ROLES if r!='qa'},
        'initial_qa':prior['qa'],'supplemental_source_review':supplement,
        'review_instruction':'Independently decide whether new original-source evidence resolves the initial blockers. Numerical Finance/Research/Scenario outputs are unchanged. Source rounding footnotes may explain display residuals only within justified precision; do not waive material contradictions or invent reconciliations. Cite original packet source IDs.'},run_dir/'qa',model,timeout)
    if result['decision']!='pass': raise RuntimeError('Independent QA re-review did not pass; no freeze')
    files=['packet.json','qa_supplement.json']
    for role in (*ROLES,'qa_initial'):
        files += [f'{role}/{name}' for name in ('input.json','prompt.txt','output.json','run.json')]
    freeze={'frozen_at':now(),'status':'assumptions_frozen_after_source_review','packet_sha256':digest(packet),
        'files':{f:hashlib.sha256((run_dir/f).read_bytes()).hexdigest() for f in files},
        'review_lineage':'Initial rejected QA retained; one additional genuine model call reviewed supplemental original-source evidence. The three upstream role outputs and numeric assumptions were not changed.',
        'disclosure':'Retrospective execution; date-filtered inputs do not erase model pretraining.'}
    write(run_dir/'freeze.json',freeze)
    return freeze

def replay(run_dir):
    """Verify frozen outputs and return assumptions. No subprocess/model/network call."""
    run_dir=Path(run_dir); freeze=read(run_dir/'freeze.json')
    for file, expected in freeze['files'].items():
        if hashlib.sha256((run_dir/file).read_bytes()).hexdigest()!=expected: raise ValueError(f'Frozen file changed: {file}')
    packet=read(run_dir/'packet.json'); validate_packet(packet)
    for role in ROLES: validate_output(role,read(run_dir/role/'output.json'),packet)
    if read(run_dir/'qa'/'output.json')['decision'] != 'pass': raise ValueError('QA did not pass')
    return {'execution':'deterministic_replay_no_model_call','freeze_sha256':digest(freeze),
            'assumptions':read(run_dir/'scenario'/'output.json')['assumptions']}

def unlock_actuals(run_dir, actuals_path):
    verified=replay(run_dir)
    return {'freeze_sha256':verified['freeze_sha256'],'unlocked_at':now(),'actuals':read(actuals_path)}

def main():
    parser=argparse.ArgumentParser(description=__doc__); sub=parser.add_subparsers(dest='command',required=True)
    for command in ('model-run','role'):
        p=sub.add_parser(command); p.add_argument('--input',required=True); p.add_argument('--output',required=True)
        p.add_argument('--model'); p.add_argument('--timeout',type=int,default=900)
        if command=='role':p.add_argument('--role',choices=ROLES,required=True)
    p=sub.add_parser('review-qa');p.add_argument('--run',required=True);p.add_argument('--supplement',required=True);p.add_argument('--model');p.add_argument('--timeout',type=int,default=900)
    p=sub.add_parser('replay');p.add_argument('--run',required=True);p.add_argument('--output')
    args=parser.parse_args()
    if args.command=='model-run': result=run_pipeline(args.input,args.output,args.model,args.timeout)
    elif args.command=='role':result=model_role(args.role,read(args.input),args.output,args.model,args.timeout)
    elif args.command=='review-qa':result=review_qa(args.run,args.supplement,args.model,args.timeout)
    else:
        result=replay(args.run)
        if args.output:write(args.output,result)
    print(json.dumps(result,indent=2))
if __name__=='__main__': main()
