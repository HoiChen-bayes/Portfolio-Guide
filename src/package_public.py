"""Whitelist a public project tree; private translations and runtime logs never enter it."""
from pathlib import Path
import json,shutil,zipfile,hashlib
ROOT=Path(__file__).resolve().parents[1];DEST=ROOT/'publish/project'
def copy(src,rel):
 dst=DEST/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
def main():
 if DEST.exists():shutil.rmtree(DEST)
 DEST.mkdir(parents=True,exist_ok=False)
 # Never copy a directory broadly: every allowed extension and location is explicit.
 for filename in ['README.md','.gitignore']:copy(ROOT/filename,filename)
 for folder,exts in [('src',{'.py','.mjs'}),('agents',{'.md'}),('config',{'.json'}),('tests',{'.py'})]:
  for f in (ROOT/folder).rglob('*'):
   if f.is_file() and f.suffix in exts and '__pycache__' not in f.parts:copy(f,f.relative_to(ROOT))
 for f in (ROOT/'docs').rglob('*'):
  if f.is_file() and f.suffix in {'.md','.json'} and 'private_zh' not in f.parts:copy(f,f.relative_to(ROOT))
 for folder in ['history','research','holdout']:
  for f in (ROOT/'data'/folder).glob('*'):
   if f.is_file() and f.suffix in {'.json','.csv'}:copy(f,f.relative_to(ROOT))
 for f in (ROOT/'data/history/sources').glob('*_tables.json'):copy(f,f.relative_to(ROOT))
 copy(ROOT/'data/README.md','data/README.md')
 for f in (ROOT/'outputs').glob('*'):
  if f.is_file() and f.suffix in {'.xlsx','.pbix','.json','.csv','.md'}:copy(f,f.relative_to(ROOT))
 # Publish only the approved native evidence captures and editable workbook.
 for filename in ['Finance_Evidence.xlsx','revenue.png','timing.png','margin.png','scenarios.png','manifest.json']:
  f=ROOT/'outputs/guide_evidence'/filename
  if f.is_file():copy(f,f.relative_to(ROOT))
 for folder in ['screenshots','qa','powerbi']:
  for f in (ROOT/'outputs'/folder).rglob('*'):
   if not f.is_file():continue
   if folder=='powerbi' and f.suffix=='.json':
    rel=f.relative_to(ROOT/'outputs'/folder)
    source_definition=any(part.endswith(('.Report','.SemanticModel')) for part in rel.parts)
    audit_names={'build_audit.json','expected_native.json','native_model.json','native_totals.json','native_forecasts.json','native_vintage_comparison.json','visual_validation.json','final_validation.json'}
    final_audit=len(rel.parts)==2 and rel.parts[0] in {'PG','TRV'} and f.name in audit_names
    restyle_audit=str(rel)=='restyle_model_invariance.json'
    if not (source_definition or final_audit or restyle_audit):continue
   if f.suffix=='.png':
    rel=f.relative_to(ROOT/'outputs'/folder)
    excel_names={'Summary','Financial_Health','Scenario_Model','Assumptions','Forecast_Comparison','Variance_Drivers','Research_Changes','Market_Evidence','Historical_Financials','Sources_and_Checks'}
    allowed_excel=folder=='screenshots' and len(rel.parts)==2 and rel.parts[0] in {'PG','TRV'} and f.stem in excel_names
    allowed_powerbi=folder=='powerbi' and len(rel.parts)==3 and rel.parts[0] in {'PG','TRV'} and rel.parts[1]=='screenshots' and f.name in {f'{i:02}.png' for i in range(1,7)}
    if not (allowed_excel or allowed_powerbi):continue
   if not any(x.startswith('.') for x in f.relative_to(ROOT).parts) and f.suffix in {'.png','.json','.pbip','.pbir','.pbism','.bim','.md'}:copy(f,f.relative_to(ROOT))
 approved=ROOT/'outputs/runs_reviewed'
 assert all((approved/f'{c}_{v}/freeze.json').exists() for c in ['PG','TRV'] for v in ['pre_history','pre_market','mid_history','mid_market'])
 for f in approved.rglob('*'):
  if f.is_file() and f.name not in ['events.jsonl','runtime.stderr.txt'] and f.suffix in {'.json','.txt'}:copy(f,Path('outputs/runs')/f.relative_to(approved))
 # Keep the real rejected QA decisions and original packets visible, without raw runtime logs.
 for c in ['PG','TRV']:
  for v in ['pre_market','mid_market']:
   for rel in ['packet.json','qa/output.json','qa/run.json']:
    f=ROOT/'outputs/runs'/f'{c}_{v}'/rel
    if f.exists():copy(f,Path('outputs/rejected_runs')/f'{c}_{v}'/rel)
 initial=ROOT/'outputs/runs/initial_market_review.json'
 if initial.exists():copy(initial,'outputs/rejected_runs/review.json')
 # Prose gets public paths; never rewrite frozen inputs, outputs, prompts, metadata or manifests.
 for f in (DEST/'docs').rglob('*.md'):
  prose=f.read_text().replace('outputs/runs_reviewed','outputs/runs')
  prose=prose.replace('outputs/runs/initial_market_review.json','outputs/rejected_runs/review.json')
  prose=prose.replace('The first archived experiment remains under `outputs/runs`. The launch command used for that original experiment predated the fresh-root default; its eight saved outputs are unchanged.', 'The selected accepted experiment is published under `outputs/runs`; rejected original market evidence is retained under `outputs/rejected_runs`. The original launch predated the fresh-root default. Frozen file bytes are unchanged.')
  prose=prose.replace('Within each role, inspect `input.json`, `prompt.txt`, `output.json`, `run.json`, `events.jsonl` and `runtime.stderr.txt`.', 'Within each public role folder, inspect `input.json`, `prompt.txt`, `output.json` and `run.json`. Raw runtime events and stderr remain private.')
  f.write_text(prose)
 (DEST/'outputs/PUBLIC_RUN_PATHS.md').write_text("# Public run paths\n\nThe accepted local run set named `outputs/runs_reviewed` is published as `outputs/runs`. All files listed in every freeze manifest preserve their exact original bytes, so replay verifies normally. Original path names inside JSON provenance are retained and refer to this mapping; they are not external links.\n\nThe four rejected original market packets and QA decisions are in `outputs/rejected_runs`. P&G source-only QA re-reviews retain `qa_initial` and their exact source supplements inside the accepted case folders. Raw runtime events and stderr are omitted; freeze verification does not depend on them.\n")
 # Public default run path points to the approved set; all copied freeze bytes remain identical.
 for f in DEST.rglob('*'):
  if f.is_file():
   assert 'private_zh' not in f.parts and f.name not in ['events.jsonl','runtime.stderr.txt']
 manifest=[{'path':str(f.relative_to(DEST)),'size':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in sorted(DEST.rglob('*')) if f.is_file()]
 (ROOT/'publish/manifest.json').write_text(json.dumps(manifest,indent=2));print('Whitelisted public files',len(manifest),'bytes',sum(x['size'] for x in manifest))
if __name__=='__main__':main()
