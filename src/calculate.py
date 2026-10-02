"""Deterministic finance arithmetic; consume only QA-approved frozen assumptions."""
import json,csv,sys,math,argparse
from pathlib import Path
from workflow import replay
ROOT=Path(__file__).resolve().parents[1]
VINTAGES=['pre_history','pre_market','mid_history','mid_market']
LABELS={'pre_history':'March · history only','pre_market':'March · market informed','mid_history':'May · history only','mid_market':'May · market informed'}
def read(p):return json.loads(Path(p).read_text())
def historical(company):
 return [r for r in read(ROOT/'data/history/history_tidy.json') if r['company']==company and r['segment']=='Consolidated' and r['period_basis']=='quarter']
def values(rows,period):return {r['metric']:r['value'] for r in rows if r['calendar_quarter']==period}
def compute(c,a,base):
 if c=='PG':
  sales=base['net_sales']*(1+a['sales_growth']);gross=sales*a['gross_margin'];sga=sales*a['sga_ratio'];oi=gross-sga;pt=oi+a['net_nonoperating_income'];tax=pt*a['effective_tax_rate'];ni=pt-tax;attrib=ni-a['noncontrolling_income'];ocf=ni*a['ocf_to_net_income'];capex=sales*a['capex_ratio']
  return dict(net_sales=sales,gross_profit=gross,sga=sga,operating_income=oi,pretax_income=pt,income_taxes=tax,net_income=ni,net_income_attributable=attrib,diluted_eps=attrib/a['diluted_shares'],operating_cash_flow=ocf,capital_expenditures=capex,free_cash_flow=ocf-capex,gross_margin=a['gross_margin'],operating_margin=oi/sales)
 nep=base['net_earned_premiums']*(1+a['earned_premium_growth']);nwp=base['net_written_premiums']*(1+a['written_premium_growth'])
 offset=base['underwriting_gain']-base['favorable_prior_year_development']-base['catastrophe_losses_signed']-base['net_earned_premiums']*(1-base['underlying_combined_ratio']/100)
 underlying=nep*(1-a['underlying_combined_ratio'])+offset;uw=underlying-a['catastrophe_losses']+a['favorable_reserve_development'];pt=uw+a['investment_income']+a['other_income_including_interest'];tax=pt*a['effective_tax_rate']
 return dict(net_earned_premiums=nep,net_written_premiums=nwp,underlying_underwriting_gain=underlying,underwriting_gain=uw,investment_income_pretax=a['investment_income'],core_pretax_income=pt,core_income_tax=tax,core_income=pt-tax,core_income_per_diluted_share_proxy=(pt-tax)/a['diluted_shares'],underlying_combined_ratio=a['underlying_combined_ratio'],combined_ratio=a['underlying_combined_ratio']+(a['catastrophe_losses']-a['favorable_reserve_development'])/nep,catastrophe_losses=a['catastrophe_losses'],favorable_prior_year_development=a['favorable_reserve_development'],basis_adjustment=offset)
def write_csv(path,rows):
 if not rows:return
 with path.open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def main(argv=()):
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--runs-dir',default='outputs/runs');args=parser.parse_args(argv)
 runs_path=Path(args.runs_dir);runs_path=runs_path if runs_path.is_absolute() else ROOT/runs_path
 out=ROOT/'outputs';out.mkdir(exist_ok=True);bundle={};flat=[];checks=[]
 # Enforce all eight freezes before this process reads any held-out values.
 for c in ['PG','TRV']:
  for v in VINTAGES:replay(runs_path/f'{c}_{v}')
 actual=read(ROOT/'data/holdout/actuals.json')['companies']
 for c in actual:actual[c]['metrics']=actual[c]['model_metrics']
 actual['TRV']['metrics']['core_income_per_diluted_share_proxy']=actual['TRV']['metrics']['core_income']/actual['TRV']['metrics']['diluted_shares']
 for c in ['PG','TRV']:
  hist=historical(c);base=values(hist,'2025Q2');runs={};forecasts=[]
  for v in VINTAGES:
   run=runs_path/f'{c}_{v}';frozen=replay(run)
   assumptions=frozen['assumptions'];runs[v]={'assumptions':assumptions,'freeze':read(run/'freeze.json'),'qa':read(run/'qa/output.json')}
   for case in ['bear','base','bull']:
    a={r['driver']:r[case] for r in assumptions};result=compute(c,a,base)
    forecasts.append(dict(vintage=v,label=LABELS[v],case=case,drivers=a,metrics=result))
    for m,n in result.items():flat.append(dict(company=c,vintage=v,label=LABELS[v],case=case,metric=m,value=n))
    checks.append(dict(company=c,check=v+' '+case+' pretax bridge',difference=(result['operating_income']+a['net_nonoperating_income']-result['pretax_income']) if c=='PG' else result['underwriting_gain']+a['investment_income']+a['other_income_including_interest']-result['core_pretax_income'],tolerance=.000001))
   profits=[f['metrics']['net_income_attributable' if c=='PG' else 'core_income'] for f in forecasts[-3:]]
   if not profits[0]<=profits[1]<=profits[2]:raise ValueError('Incoherent profit case order '+c+v)
  # Actuals schema is company -> metric dictionary; original records remain separately traceable.
  av=actual[c]['metrics'];variances=[]
  for f in forecasts:
   for m,n in f['metrics'].items():
    if m not in av:continue
    d=av[m]-n;variances.append(dict(vintage=f['vintage'],case=f['case'],metric=m,forecast=n,actual=av[m],difference=d,relative_difference=d/abs(n) if n else None))
  # One-at-a-time numerical sensitivities; these are model mechanics, not calibrated probabilities.
  chosen=next(f for f in forecasts if f['vintage']=='mid_market' and f['case']=='base');metric='net_income_attributable' if c=='PG' else 'core_income';sens=[]
  shocks=({'sales_growth':.01,'gross_margin':.01,'sga_ratio':.01,'effective_tax_rate':.01} if c=='PG' else {'earned_premium_growth':.01,'underlying_combined_ratio':.01,'catastrophe_losses':100,'investment_income':100})
  for d,s in shocks.items():
   a=chosen['drivers'].copy();a[d]+=s;sens.append(dict(driver=d,shock=s,profit_change=compute(c,a,base)[metric]-chosen['metrics'][metric]))
  # Sequential bridge connects the two same-history forecasts; order explicitly disclosed.
  bridges=[]
  for prefix in ['pre','mid']:
   old=next(f for f in forecasts if f['vintage']==prefix+'_history' and f['case']=='base');new=next(f for f in forecasts if f['vintage']==prefix+'_market' and f['case']=='base');a=old['drivers'].copy();last=old['metrics'][metric]
   for driver in a:
    a[driver]=new['drivers'][driver];nextval=compute(c,a,base)[metric];bridges.append(dict(vintage=prefix,driver=driver,profit_change=nextval-last));last=nextval
   checks.append(dict(company=c,check=prefix+' research bridge',difference=last-new['metrics'][metric],tolerance=1e-6))
  if c=='PG':
   actual_drivers=dict(sales_growth=av['net_sales']/base['net_sales']-1,gross_margin=av['gross_profit']/av['net_sales'],sga_ratio=av['sga']/av['net_sales'],net_nonoperating_income=av['net_nonoperating_income'],effective_tax_rate=av['income_taxes']/av['pretax_income'],noncontrolling_income=av['noncontrolling_income'],diluted_shares=av['diluted_shares'],ocf_to_net_income=av['operating_cash_flow']/av['net_income'],capex_ratio=av['capital_expenditures']/av['net_sales'])
  else:
   actual_drivers=dict(earned_premium_growth=av['net_earned_premiums']/base['net_earned_premiums']-1,written_premium_growth=av['net_written_premiums']/base['net_written_premiums']-1,underlying_combined_ratio=av['underlying_combined_ratio'],catastrophe_losses=av['catastrophe_losses'],favorable_reserve_development=av['favorable_prior_year_development'],investment_income=av['investment_income_pretax'],other_income_including_interest=av['other_income_including_interest'],effective_tax_rate=av['core_income_tax']/av['core_pretax_income'],diluted_shares=av['diluted_shares'])
  actual_bridge=[];a=chosen['drivers'].copy();last=chosen['metrics'][metric]
  for driver in a:
   a[driver]=actual_drivers[driver];n=compute(c,a,base)[metric];actual_bridge.append(dict(driver=driver,profit_change=n-last));last=n
  actual_bridge.append(dict(driver='Reported rounding and basis residual',profit_change=av[metric]-last))
  checks.append(dict(company=c,check='May base to actual profit bridge',difference=chosen['metrics'][metric]+sum(r['profit_change'] for r in actual_bridge)-av[metric],tolerance=1e-6))
  accuracy=[]
  for v in VINTAGES:
   ff=[f for f in forecasts if f['vintage']==v];basef=ff[1]['metrics'][metric];accuracy.append(dict(vintage=v,base_profit=basef,actual_profit=av[metric],absolute_error=abs(basef-av[metric]),absolute_percentage_error=abs(basef-av[metric])/abs(av[metric]),inside_scenario_range=ff[0]['metrics'][metric]<=av[metric]<=ff[2]['metrics'][metric]))
  balance=[r for r in read(ROOT/'data/history/history_tidy.json') if r['company']==c and r['segment']=='Consolidated' and r['period_basis']=='instant']
  previous=values(hist,'2026Q1');prior_year=values(hist,'2025Q1');diagnostics=[]
  revenue='net_sales' if c=='PG' else 'net_earned_premiums'
  for m in [revenue,metric,'operating_cash_flow']:
   if m in previous and m in prior_year:diagnostics.append(dict(metric=m,previous_quarter=previous[m],prior_year_same_quarter=prior_year[m],growth=previous[m]/prior_year[m]-1 if prior_year[m] else None))
  bundle[c]=dict(company=c,base=base,history=hist,balance_history=balance,previous_quarter_diagnostics=diagnostics,actual=actual[c],actual_drivers=actual_drivers,actual_bridge=actual_bridge,accuracy=accuracy,runs=runs,forecasts=forecasts,variances=variances,sensitivity=sens,research_bridges=bridges)
 if any(abs(r['difference'])>r['tolerance'] for r in checks):raise ValueError('Arithmetic check failed')
 (out/'analysis.json').write_text(json.dumps(bundle,indent=2,allow_nan=False));write_csv(out/'forecast_results.csv',flat);write_csv(out/'calculation_checks.csv',checks)
 (out/'calculation_checks.json').write_text(json.dumps(checks,indent=2));print('Validated',len(checks),'arithmetic checks;',len(flat),'forecast metric rows')
if __name__=='__main__':main(sys.argv[1:])
