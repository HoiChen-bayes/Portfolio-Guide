"""Create cutoff-controlled forecast inputs from curated source datasets (no actuals)."""
import json
from pathlib import Path
from workflow import validate_packet, write
ROOT=Path(__file__).resolve().parents[1]
CONTRACTS={
'PG':[('sales_growth','decimal',-.15,.20),('gross_margin','decimal',.35,.60),('sga_ratio','decimal',.20,.35),('net_nonoperating_income','USD million',-500,800),('effective_tax_rate','decimal',.10,.35),('noncontrolling_income','USD million',0,100),('diluted_shares','million shares',2200,2700),('ocf_to_net_income','decimal',.5,2.5),('capex_ratio','decimal',.03,.10)],
'TRV':[('earned_premium_growth','decimal',-.15,.2),('written_premium_growth','decimal',-.15,.2),('underlying_combined_ratio','decimal',.75,1.0),('catastrophe_losses','USD million',0,4000),('favorable_reserve_development','USD million',0,1000),('investment_income','USD million',600,1500),('other_income_including_interest','USD million',-300,100),('effective_tax_rate','decimal',.1,.3),('diluted_shares','million shares',190,240)]}
MODEL_NOTES={
'PG':'Sales are same-quarter prior-year net_sales*(1+sales_growth). Operating income=sales*(gross_margin-sga_ratio); pretax=operating+net_nonoperating_income; attributable net income=pretax*(1-effective_tax_rate)-noncontrolling_income; EPS=attributable NI/diluted shares. OCF=total net income*ocf_to_net_income; capex=sales*capex_ratio, positive outflow. Historical diluted shares may be approximated by NI attributable/diluted EPS; disclose rounding. Gross margin and SG&A are fractions of sales. Noncontrolling interest=total NI-NI attributable. Net nonoperating=interest_income+signed interest_expense+other_income. Cash conversion and capex require seasonality caveats; no debt/cash bridge or operational units/headcount forecast is supported.',
'TRV':'Premium growth is same-quarter-prior-year net_earned_premiums/net_written_premiums growth. Core pretax=NEP*(1-underlying_combined_ratio)-catastrophe_losses+favorable_reserve_development+investment_income+other_income_including_interest. Core net income=core pretax*(1-effective_tax_rate); core EPS=core NI/diluted_shares. Cats are positive losses; reserve development positive is favorable. Percent ratios become decimal. Historical core tax/core pretax gives tax rate. Ratio rounding and reporting-basis differences mean underwriting dollars need a residual reconciliation; do not claim exact GAAP underwriting tie. No supported cash-flow/debt/capital projection; acknowledge thin coverage.'}

MODEL_NOTES['TRV'] += ' Add a fixed same-quarter-prior-year underwriting basis adjustment: historical underwriting_gain - favorable_prior_year_development - catastrophe_losses_signed - net_earned_premiums*(1-underlying_combined_ratio/100). This offset represents fees/reporting-basis differences and is held fixed across scenarios, never fitted to target. Core income is the main earnings output; do not rely on simple EPS as reported EPS because participating/preferred adjustments are not modeled.'

def build():
 history=json.loads((ROOT/'data/history/history_tidy.json').read_text())
 evidence=json.loads((ROOT/'data/research/market_evidence.json').read_text())['records']
 out=ROOT/'data/packets';out.mkdir(exist_ok=True)
 for company in CONTRACTS:
  for vintage in ('pre_history','pre_market','mid_history','mid_market'):
   cutoff='2026-03-31' if vintage.startswith('pre') else '2026-05-15'
   selected={}
   for r in history:
    if r['company']!=company or r['segment']!='Consolidated' or r['period_basis']!='quarter':continue
    if not '2025-01-01'<=r['period_end']<'2026-04-01' or r['publication_date']>cutoff:continue
    key=(r['period_end'],r['metric'])
    if key not in selected or r['publication_date']>selected[key]['publication_date']:selected[key]=r
   rows=[]
   keys=('source_id','source_url','source_locator','source_excerpt','period_start','period_end','metric','value','unit','value_status','notes')
   for r in selected.values():
    row={k:r[k] for k in keys if k in r};row['published_at']=r['publication_date'];rows.append(row)
   evid=[]
   if vintage.endswith('market'):
    evid=[dict(r,source_id=r['id']) for r in evidence if r['company']==company and r['published_at']<=cutoff and not r.get('excluded_from_model',False)]
   packet={'company':company,'sector':'consumer products' if company=='PG' else 'property/casualty insurance','vintage':vintage,'cutoff':cutoff,
    'target_period':{'start':'2026-04-01','end':'2026-06-30'},'history':rows,'evidence':evid,
    'driver_contract':[{'driver':d,'unit':u,'min':lo,'max':hi} for d,u,lo,hi in CONTRACTS[company]],
    'model_contract':MODEL_NOTES[company],
    'analysis_scope':'Analyst-defined illustrative scenario model, not official company budget. Derive defensible base from eligible history; bear/bull are adverse/favorable profitability scenarios, not numeric ascending for every driver. Contract bounds are broad guardrails, not prescribed forecast estimates. All market-to-financial mappings are analyst judgments. Finance should map only financially material reference rows (latest history, same-quarter-prior-year baseline, and supporting trends), not repeat every row. No final-period outcomes are supplied. Missing detailed cash, debt, exposure, or portfolio breakdowns must be limitations, not invented observed facts. QA evaluates a transparent illustrative model; uncertainty alone is not an error, but unsupported claims of certainty are.'}
   validate_packet(packet);write(out/f'{company}_{vintage}.json',packet)
if __name__=='__main__':build()
