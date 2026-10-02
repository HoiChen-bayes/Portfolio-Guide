"""Run two genuine model pipelines at a time, always in a new immutable run root."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from workflow import read, write, run_pipeline
ROOT=Path(__file__).resolve().parents[1]

def run(company,vintage,run_root,model=None):
 packet_path=run_root/'prepared_packets'/f'{company}_{vintage}.json'
 out=run_root/f'{company}_{vintage}'
 if vintage.endswith('market'):
  control=vintage.replace('market','history');control_out=run_root/f'{company}_{control}'
  if not (control_out/'freeze.json').exists():return {'case':out.name,'status':'blocked_control_not_frozen'}
  packet=read(packet_path)
  packet['history_control_assumptions']=read(control_out/'scenario/output.json')['assumptions']
  packet['comparison_instruction']='Use this frozen history-only control as the counterfactual. Explain incremental changes driven by eligible market evidence; leave unrelated drivers unchanged unless a specific justified correction is necessary. Market research uncertainty can widen scenarios without forcing base changes.'
  write(packet_path,packet)
 try:
  run_pipeline(packet_path,out,model=model,timeout=900)
  return {'case':out.name,'status':'frozen'}
 except Exception as exc:return {'case':out.name,'status':'failed','error':str(exc)}

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--run-root',type=Path,help='New directory; defaults to outputs/runs_<UTC timestamp>')
 parser.add_argument('--packets-dir',type=Path,default=ROOT/'data/packets')
 parser.add_argument('--model',help='Optional model override; default inherits user configuration')
 args=parser.parse_args()
 run_root=(args.run_root or ROOT/'outputs'/('runs_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))).resolve()
 run_root.mkdir(parents=True,exist_ok=False)
 (run_root/'prepared_packets').mkdir()
 for company in ('PG','TRV'):
  for vintage in ('pre_history','mid_history','pre_market','mid_market'):
   packet=read(args.packets_dir/f'{company}_{vintage}.json')
   packet.pop('history_control_assumptions',None);packet.pop('comparison_instruction',None)
   write(run_root/'prepared_packets'/f'{company}_{vintage}.json',packet)
 summary=[]
 print(f'New model-run root: {run_root}',flush=True)
 for vintage in ('pre_history','mid_history','pre_market','mid_market'):
  with ThreadPoolExecutor(max_workers=2) as pool:
   futures=[pool.submit(run,c,vintage,run_root,args.model) for c in ('PG','TRV')]
   for future in as_completed(futures):
    item=future.result();summary.append(item);print(item,flush=True)
    write(run_root/'batch_status.json',summary)
 if any(r['status']!='frozen' for r in summary):raise SystemExit(1)
if __name__=='__main__':main()
