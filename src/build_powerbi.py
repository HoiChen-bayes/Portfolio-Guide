"""Build portable native PBIP reports from the frozen, validated analysis snapshot."""
from pathlib import Path
import json,uuid,hashlib,math,datetime
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'outputs/powerbi';ANALYSIS=ROOT/'outputs/analysis.json'
base='https://developer.microsoft.com/json-schemas/';pref='fabric/item/report/definition/'
def dump(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2),encoding='utf-8')
def dv(v):
 if v is None:return 'BLANK()'
 if isinstance(v,str):return '"'+v.replace('"','""').replace('\n',' ')+'"'
 return str(v)
def build(co,data):
 global REPORT,SM,pages,visual_count,bindings,tables,types,measures,INK,ACCENT,BG
 name=('PAndG' if co=='PG' else 'Travelers')+'_Scenarios';dest=OUT/co;REPORT=dest/(name+'.Report');SM=dest/(name+'.SemanticModel');pages=[];visual_count=0;bindings=[]
 INK='#142F66' if co=='PG' else '#242A30';ACCENT='#1459D9' if co=='PG' else '#C71932';BG='#F2F6FC' if co=='PG' else '#F4F4F4';tables={};types={}
 def ds(n,cols,rows):types[n]=cols;tables[n]=rows
 rev='net_sales' if co=='PG' else 'net_earned_premiums';profit='net_income_attributable' if co=='PG' else 'core_income';op='operating_income' if co=='PG' else 'underwriting_gain';margin='operating_margin' if co=='PG' else 'combined_ratio'
 vintages=[('pre_history','March | History only',1),('pre_market','March | Market informed',2),('mid_history','May | History only',3),('mid_market','May | Market informed',4)]
 ds('Vintage',[('Vintage','string'),('VintageLabel','string'),('Sort','int64')],vintages);ds('VintageCompare',[('Vintage','string'),('VintageLabel','string'),('Sort','int64')],vintages);ds('Scenario',[('Case','string'),('Sort','int64')],[['bear',1],['base',2],['bull',3]])
 ds('Forecast',[('Vintage','string'),('Case','string'),('Revenue','double'),('Profit','double'),('Operating','double'),('Margin','double'),('Liquidity','double')],[[f['vintage'],f['case'],f['metrics'][rev],f['metrics'][profit],f['metrics'][op],f['metrics'][margin],f['metrics'].get('free_cash_flow',f['metrics'].get('catastrophe_losses'))] for f in data['forecasts']])
 av=data['actual']['metrics'];ds('Actual',[('Revenue','double'),('Profit','double'),('Operating','double'),('Margin','double')],[[av[rev],av[profit],av[op],av[margin]]])
 historical={}
 for r in data['history']:historical.setdefault(r['calendar_quarter'],{})[r['metric']]=r['value']
 ds('History',[('Quarter','string'),('Revenue','double'),('Profit','double'),('Operating','double'),('Ratio','double'),('CashFlow','double')],[[q,d.get(rev),d.get(profit),d.get(op),d.get('gross_profit',0)/d.get('net_sales',1) if co=='PG' else d.get('combined_ratio',0)/100,d.get('operating_cash_flow')] for q,d in sorted(historical.items())])
 allhist=json.loads((ROOT/'data/history/history_tidy.json').read_text());segmetric='net_sales' if co=='PG' else 'net_written_premiums'
 ds('Segments',[('Segment','string'),('Amount','double')],[[r['segment'],r['value']] for r in allhist if r['company']==co and r['calendar_quarter']=='2026Q1' and r['metric']==segmetric and r['segment']!='Consolidated' and r['period_basis']=='quarter'])
 ds('Bridge',[('Window','string'),('Driver','string'),('ProfitChange','double'),('Sort','int64')],[[r['vintage'],r['driver'].replace('_',' '),r['profit_change'],i%max(1,len(data['research_bridges'])//2)] for i,r in enumerate(data['research_bridges'])])
 ds('ActualBridge',[('Driver','string'),('ProfitChange','double'),('Sort','int64')],[[r['driver'].replace('_',' '),r['profit_change'],i] for i,r in enumerate(data.get('actual_bridge',[]))])
 ds('Sensitivity',[('Driver','string'),('Shock','double'),('ProfitChange','double')],[[r['driver'].replace('_',' '),r['shock'],r['profit_change']] for r in data['sensitivity']])
 ds('Comparison',[('Vintage','string'),('Case','string'),('Metric','string'),('Forecast','double'),('Actual','double'),('Difference','double'),('ErrorPercent','double')],[[r['vintage'],r['case'],r['metric'].replace('_',' '),r['forecast'],r['actual'],r['difference'],r['relative_difference']] for r in data['variances'] if 'ratio' not in r['metric'] and 'margin' not in r['metric'] and r['metric'] not in ['diluted_eps','core_income_per_diluted_share_proxy']])
 ds('Drivers',[('Vintage','string'),('Case','string'),('Driver','string'),('Value','double')],[[f['vintage'],f['case'],d.replace('_',' '),v] for f in data['forecasts'] for d,v in f['drivers'].items()])
 qa=[]
 for v,run in data['runs'].items():
  qa.append([v,'QA approval',str(run['qa'].get('decision','unavailable')),str(run['qa'].get('source_accuracy','Not assessed'))])
  for f in run['qa'].get('findings',[]):
   if f.get('severity') in ['warning','error']:qa.append([v,f.get('subject','QA finding'),f.get('severity','finding'),f.get('finding','')])
 qa += [['All','Source dates','Passed','Financial periods through March 2026; publication gates March 31 / May 15'],['All','Retrospective reconstruction','Disclosed','Runs executed today; do not claim forecasts were authored before the target'],['All','Accounting identity','Passed','72 historical checks; rounding tolerance retained'],['All','Actual holdout','Separated','Targets loaded only after model assumption freeze'],['All','Model basis','Illustrative','Analyst scenarios, not company guidance or official budget'],['All','Liquidity boundary','Limited','PG cash conversion assumption; TRV liquidity is not a retail cash budget']]
 ds('QA',[('Vintage','string'),('Check','string'),('Status','string'),('Detail','string')],qa)
 ds('Sources',[('Quarter','string'),('Metric','string'),('Published','string'),('SourceURL','string')],[[r['calendar_quarter'],r['metric'].replace('_',' '),r['publication_date'],r['source_url']] for r in data['history'] if r['metric'] in [rev,profit,'operating_cash_flow']])
 measures={}
 for col in ['Revenue','Profit','Operating','Margin','Liquidity']:
  measures['Selected '+col]='VAR V=SELECTEDVALUE(Vintage[Vintage],"mid_market") VAR C=SELECTEDVALUE(Scenario[Case],"base") RETURN CALCULATE(MAX(Forecast['+col+']),KEEPFILTERS(Vintage[Vintage]=V),KEEPFILTERS(Scenario[Case]=C))'
  if col!='Liquidity':measures['Actual '+col]='MAX(Actual['+col+'])'
 measures.update({'Vintage profit':'CALCULATE([Selected Profit],REMOVEFILTERS(Vintage),TREATAS(VALUES(VintageCompare[Vintage]),Vintage[Vintage]))','Profit error':'[Actual Profit]-[Selected Profit]','Profit error %':'DIVIDE([Profit error],[Selected Profit])','History revenue':'SUM(History[Revenue])','History profit':'SUM(History[Profit])','History operating':'SUM(History[Operating])','History cash flow':'SUM(History[CashFlow])','History ratio':'AVERAGE(History[Ratio])','Segment value':'SUM(Segments[Amount])','Bridge impact':'CALCULATE(SUM(Bridge[ProfitChange]),KEEPFILTERS(Bridge[Window]=SELECTEDVALUE(Bridge[Window],"mid")))','Actual bridge impact':'SUM(ActualBridge[ProfitChange])','Sensitivity impact':'SUM(Sensitivity[ProfitChange])','Forecast comparison':'SUM(Comparison[Forecast])','Actual comparison':'SUM(Comparison[Actual])','Difference comparison':'SUM(Comparison[Difference])','QA rows':'COUNTROWS(QA)'})
 measures['Free cash flow' if co=='PG' else 'Catastrophe losses']='[Selected Liquidity]'
 percent={'Selected Margin','Actual Margin','Profit error %','History ratio'};money='$#,0.0;($#,0.0);$0.0'
 models=[]
 for n,cols in types.items():
  columns=[{'name':c,'dataType':t,'sourceColumn':'['+c+']','summarizeBy':'none','type':'calculatedTableColumn',**({'formatString':('0.0%' if c in ['Margin','Ratio','ErrorPercent'] else money)} if t=='double' and c not in ['Value','Shock'] else {})} for c,t in cols]
  if n in ['Bridge','ActualBridge']:
   for c in columns:
    if c['name']=='Driver':c['sortByColumn']='Sort'
  if n=='Sources':
   for c in columns:
    if c['name']=='SourceURL':c['dataCategory']='WebUrl'
  if n in ['Vintage','VintageCompare','Scenario']:
   for c in columns:
    if c['name'] in ['VintageLabel','Case']:c['sortByColumn']='Sort'
  expr='DATATABLE('+','.join('"'+c+'",'+{'string':'STRING','double':'DOUBLE','int64':'INTEGER'}[t] for c,t in cols)+',{'+','.join('{'+','.join(dv(v) for v in r)+'}' for r in tables[n])+'})'
  models.append({'name':n,'columns':columns,'partitions':[{'name':n,'mode':'import','source':{'type':'calculated','expression':expr}}]})
 models[[m['name'] for m in models].index('Forecast')]['measures']=[{'name':n,'expression':e,'formatString':'0.0%;(0.0%);0.0%' if n in percent else '0' if n=='QA rows' else money} for n,e in measures.items()]
 rels=[]
 for fact in ['Forecast','Comparison','Drivers']:
  for dim,key in [('Vintage','Vintage'),('Scenario','Case')]:rels.append({'name':str(uuid.uuid5(uuid.NAMESPACE_DNS,co+fact+dim)),'fromTable':fact,'fromColumn':key,'toTable':dim,'toColumn':key,'fromCardinality':'many','toCardinality':'one','crossFilteringBehavior':'oneDirection'})
 dump(SM/'model.bim',{'name':name,'compatibilityLevel':1606,'model':{'culture':'en-US','defaultPowerBIDataSourceVersion':'powerBI_V3','defaultMode':'import','tables':models,'relationships':rels}})
 dump(SM/'definition.pbism',{'version':'1.0','settings':{'qnaEnabled':False}});dump(dest/(name+'.pbip'),{'version':'1.0','artifacts':[{'report':{'path':name+'.Report'}}],'settings':{'enableAutoRecovery':True}});dump(REPORT/'definition.pbir',{'version':'4.0','datasetReference':{'byPath':{'path':'../'+name+'.SemanticModel'}}});dump(REPORT/'definition/version.json',{'$schema':base+pref+'versionMetadata/1.0.0/schema.json','version':'2.0.0'})
 dump(REPORT/'StaticResources/RegisteredResources/ScenarioTheme.json',{'name':name,'dataColors':[ACCENT,'#3EA5D9' if co=='PG' else '#5B6570','#E6A23C','#168A70','#936DCC'],'background':BG,'foreground':INK,'tableAccent':ACCENT,'good':'#168A70','bad':'#C71932'})
 dump(REPORT/'definition/report.json',{'$schema':base+pref+'report/3.1.0/schema.json','themeCollection':{'customTheme':{'name':'ScenarioTheme.json','reportVersionAtImport':{'visual':'2.1.0','page':'2.0.0','report':'3.1.0'},'type':'RegisteredResources'}},'resourcePackages':[{'name':'RegisteredResources','type':'RegisteredResources','items':[{'name':'ScenarioTheme.json','path':'ScenarioTheme.json','type':'CustomTheme'}]}],'settings':{'useEnhancedTooltips':True}})
 revenue_label='Net sales' if co=='PG' else 'Earned premiums';profit_label='Net income attributable' if co=='PG' else 'Core income';brand='P&G' if co=='PG' else 'TRAVELERS'
 p=page('01_Summary',('01  P&G | Summary' if co=='PG' else '01  Travelers | Underwriting'),brand+'  /  APR–JUN 2026  /  USD millions  /  retrospective scenario study')
 filters(p)
 if co=='PG':
  for x,m,title in [(30,'Selected Revenue','Forecast '+revenue_label),(382,'Selected Profit','Forecast '+profit_label),(734,'Selected Margin','Operating margin'),(1086,'Profit error','Actual minus forecast profit')]:card(p,m,title,x,210,324)
  chart(p,C('VintageCompare','VintageLabel'),['Vintage profit','Actual Profit'],'Four information sets vs actual | selected case',30,362,680,315,'clusteredColumnChart')
  chart(p,C('History','Quarter'),['History revenue'],'Nine-quarter financial history',730,362,680,315)
  textbox(p,'Choose a vintage and case above. Default: May market-informed base. Profit deviation = (actual - forecast) / forecast; it is not an accuracy score.',30,707,1380,68,16)
  textbox(p,'Consumer products: sales, gross margin, SG&A and cash conversion.',30,796,1380,100,19)
 else:
  for y,m,title in [(210,'Selected Profit','FORECAST CORE INCOME'),(367,'Selected Margin','FORECAST COMBINED RATIO'),(524,'Catastrophe losses','FORECAST CATASTROPHE LOSSES'),(681,'Profit error','PROFIT DEVIATION | USDm')]:
   o=card(p,m,title,30,y,325)
   o['visual']['visualContainerObjects']['background'][0]['properties']['color']=color('#242A30')
   o['visual']['visualContainerObjects']['title'][0]['properties']['fontColor']=color('#FFFFFF')
   o['visual']['objects']['labels'][0]['properties']['color']=color('#FFFFFF')
   dump(p/'visuals'/o['name']/'visual.json',o)
  chart(p,C('VintageCompare','VintageLabel'),['Vintage profit','Actual Profit'],'UNDERWRITING OUTLOOK | four information sets vs actual',380,210,1030,350,'clusteredColumnChart')
  chart(p,C('History','Quarter'),['History revenue'],'EARNED PREMIUMS | nine-quarter operating scale',380,585,1030,240)
  textbox(p,'Risk panel: underlying loss performance, catastrophes and reserve development. Default: May market-informed base. Profit deviation is actual minus forecast.',30,851,1380,80,16)
 p=page('02_History','02  History & segments','As-reported historical financials | Quarter dates and publication dates are different')
 chart(p,C('History','Quarter'),['History revenue','History profit'],'Revenue and profit | USDm',30,130,850,315)
 visual(p,'treemap',900,130,510,315,'2026Q1 segment '+('sales' if co=='PG' else 'written premiums'),{'Group':[C('Segments','Segment')],'Values':[M('Segment value')]})
 chart(p,C('History','Quarter'),['History cash flow'],'Operating cash flow | missing observations stay blank',30,470,680,315,'clusteredColumnChart')
 chart(p,C('History','Quarter'),['History ratio'],'Gross margin' if co=='PG' else 'Reported combined ratio',730,470,680,315)
 textbox(p,'March 2026 results were published in April: excluded from the March vintage, available to both May controls. Segment snapshot: calendar 2026Q1.',30,815,1380,88,16)
 p=page('03_Scenarios','03  Scenario range','Analyst-defined bear / base / bull | Not probabilities, official guidance or company budgets')
 filters(p)
 chart(p,C('Scenario','Case'),['Selected Revenue','Selected Profit'],'Scenario revenue and profit | selected vintage',30,220,680,310,'clusteredColumnChart')
 visual(p,'scatterChart',730,220,680,310,'Risk / return view | cases by revenue and profit',{'Category':[C('Scenario','Case')],'X':[M('Selected Revenue')],'Y':[M('Selected Profit')],'Size':[M('Selected Operating')],'Tooltips':[M('Selected Margin')]})
 table(p,[C('Vintage','VintageLabel'),C('Scenario','Case'),M('Selected Revenue'),M('Selected Profit'),M('Selected Margin'),M('Free cash flow' if co=='PG' else 'Catastrophe losses')],'Scenario matrix | cash generation' if co=='PG' else 'Scenario matrix | insurance loss drivers',30,555,1380,345)
 p=page('04_Market','04  Market revisions','Same-history attribution | Sequential driver replacement; ordering affects individual contributions')
 slicer(p,'Bridge','Window','Information window: pre / mid',30,115,430,90)
 visual(p,'waterfallChart',30,225,850,355,'Market-research change in profit | USDm',{'Category':[C('Bridge','Driver')],'Y':[M('Bridge impact')]})
 chart(p,C('Sensitivity','Driver'),['Sensitivity impact'],'One-at-a-time sensitivity | May base',905,225,505,355,'clusteredBarChart')
 table(p,[C('Sensitivity','Driver'),C('Sensitivity','Shock'),M('Sensitivity impact')],'Shock sizes: ratio +0.01; dollar driver +$100m',30,605,1380,230)
 textbox(p,'Research effects compare history-only and market-informed cases using identical financial history. History refresh is a separate comparison. Sensitivities are mechanics, not forecasts.',30,850,1380,84,15)
 p=page('05_Actual','05  Forecast vs actual','Held-out target: calendar 2026Q2 | Compare like-for-like measures, with source rounding retained')
 filters(p)
 for x,m,title in [(30,'Selected Profit','Forecast '+profit_label),(495,'Actual Profit','Actual '+profit_label),(960,'Profit error %','Profit deviation')]:card(p,m,title,x,210,450)
 chart(p,C('VintageCompare','VintageLabel'),['Vintage profit','Actual Profit'],'All information sets vs held-out profit',30,365,680,310,'clusteredColumnChart')
 visual(p,'waterfallChart',730,365,680,310,'May base to actual | profit driver effects',{'Category':[C('ActualBridge','Driver')],'Y':[M('Actual bridge impact')]})
 table(p,[C('Comparison','Vintage'),C('Comparison','Case'),C('Comparison','Metric'),C('Comparison','Forecast'),C('Comparison','Actual'),C('Comparison','Difference'),C('Comparison','ErrorPercent')],'Signed differences | Actual - Forecast; relative = difference / |forecast|; neutral cost/revenue coloring',30,705,1380,210)
 p=page('06_Method','06  Method & QA','Source-date gates + four model roles + deterministic arithmetic + frozen assumptions + separate actual holdout')
 table(p,[C('QA','Check'),C('QA','Status'),C('QA','Detail')],'Validation and interpretation',30,130,1380,410)
 table(p,[C('Sources','Quarter'),C('Sources','Metric'),C('Sources','Published'),C('Sources','SourceURL')],'Official source lineage | stored snapshot, no automatic refresh',30,565,1380,290)
 textbox(p,'Finance → Research → Scenario → QA. Model rerun differs from deterministic replay. Target-release snippet exposure by coordinator / collector is disclosed; forecasting roles receive eligible packets only.',30,875,1380,82,14)
 dump(REPORT/'definition/pages/pages.json',{'$schema':base+pref+'pagesMetadata/1.0.0/schema.json','pageOrder':pages,'activePageName':pages[0]})
 for t,n,m in bindings:assert t in tables and (n in measures if m else n in dict(types[t])),(t,n,m)
 dump(dest/'build_audit.json',{'company':co,'built_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'analysis_sha256':hashlib.sha256(ANALYSIS.read_bytes()).hexdigest(),'tables':{n:len(r) for n,r in tables.items()},'pages':len(pages),'visuals':visual_count,'measures':len(measures),'bindings':len(bindings),'native_desktop_validation':'pending'})
 # Reference expected DAX totals for native verification.
 chosen=next(f for f in data['forecasts'] if f['vintage']=='mid_market' and f['case']=='base')
 dump(dest/'expected_native.json',{'Revenue':chosen['metrics'][rev],'Profit':chosen['metrics'][profit],'Operating':chosen['metrics'][op],'Margin':chosen['metrics'][margin],'ActualRevenue':av[rev],'ActualProfit':av[profit],'HistoryRevenue':sum(x.get(rev,0) for x in historical.values())})
 print(co,len(pages),'pages',visual_count,'visuals')
def lit(v):return {'expr':{'Literal':{'Value':('true' if v else 'false') if isinstance(v,bool) else str(v)+'D' if isinstance(v,(int,float)) else "'"+v.replace("'","''")+"'"}}}
def color(c):return {'solid':{'color':lit(c)}}
def field(t,n,m=False):return {('Measure' if m else 'Column'):{'Expression':{'SourceRef':{'Entity':t}},'Property':n}}
def C(t,n):return (t,n,False)
def M(n):return ('Forecast',n,True)
def visual(p,typ,x,y,w,h,title='',roles=None,objects=None):
 global visual_count
 visual_count+=1;name='v'+str(visual_count).zfill(4)
 o={'$schema':base+pref+'visualContainer/2.1.0/schema.json','name':name,'position':{'x':x,'y':y,'z':visual_count,'height':h,'width':w,'tabOrder':visual_count},'visual':{'visualType':typ,'drillFilterOtherVisuals':True}}
 if roles:
  o['visual']['query']={'queryState':{k:{'projections':[{'field':field(*a),'queryRef':a[0]+'.'+a[1],'nativeQueryRef':a[1]} for a in v]} for k,v in roles.items()}};bindings.extend(a for v in roles.values() for a in v)
 if roles and 'Category' in roles and typ!='scatterChart':o['visual']['query']['sortDefinition']={'sort':[{'field':field(*roles['Category'][0]),'direction':'Ascending'}]}
 o['visual']['visualContainerObjects']={'title':[{'properties':{'show':lit(bool(title)),'text':lit(title),'fontColor':color(INK),'fontSize':lit(13)}}],'background':[{'properties':{'show':lit(True),'color':color('#FFFFFF'),'transparency':lit(0)}}],'border':[{'properties':{'show':lit(ACCENT=='#1459D9'),'color':color('#E0E8F6'),'radius':lit(12 if ACCENT=='#1459D9' else 0)}}]}
 if objects:o['visual']['objects']=objects
 dump(p/'visuals'/name/'visual.json',o);return o
def textbox(p,text,x,y,w,h,size=14,c=None):return visual(p,'textbox',x,y,w,h,objects={'general':[{'properties':{'paragraphs':[{'textRuns':[{'value':text,'textStyle':{'fontSize':str(size)+'pt','fontFamily':'Segoe UI','color':c or INK}}]}]}}]})
def page(n,title,sub):
 p=REPORT/'definition/pages'/n;pages.append(n);dump(p/'page.json',{'$schema':base+pref+'page/2.0.0/schema.json','name':n,'displayName':title,'displayOption':'FitToPage','width':1440,'height':960,'objects':{'background':[{'properties':{'color':color(BG),'transparency':lit(0)}}]}});textbox(p,title,30,12,1380,56,24,ACCENT);textbox(p,sub,30,69,1380,42,13,'#586678');return p
def card(p,m,t,x,y,w):return visual(p,'card',x,y,w,130,t,{'Values':[M(m)]},{'labels':[{'properties':{'fontSize':lit(29),'color':color(INK),'labelDisplayUnits':lit(1)}}],'categoryLabels':[{'properties':{'show':lit(False)}}]})
def chart(p,c,ms,t,x,y,w,h,typ='lineChart'):
 return visual(p,typ,x,y,w,h,t,{'Category':[c],'Y':[M(m) for m in ms]},{'categoryAxis':[{'properties':{'fontSize':lit(12),'fontColor':color(INK)}}],'valueAxis':[{'properties':{'fontSize':lit(11),'labelDisplayUnits':lit(1)}}],'legend':[{'properties':{'fontSize':lit(11)}}]})
def table(p,cols,t,x,y,w,h):return visual(p,'tableEx',x,y,w,h,t,{'Values':cols},{'grid':[{'properties':{'textSize':lit(12),'rowPadding':lit(7)}}],'columnHeaders':[{'properties':{'fontColor':color(INK),'backColor':color('#E8EDF3'),'fontSize':lit(12)}}],'total':[{'properties':{'totals':lit(False)}}]})
def slicer(p,t,c,title,x,y,w,h):return visual(p,'slicer',x,y,w,h,title,{'Values':[C(t,c)]},{'selection':[{'properties':{'singleSelect':lit(True)}}],'header':[{'properties':{'show':lit(False)}}],'items':[{'properties':{'fontSize':lit(12)}}],'data':[{'properties':{'mode':lit('Dropdown')}}]})
def filters(p):slicer(p,'Vintage','VintageLabel','Information vintage',30,115,870,75);slicer(p,'Scenario','Case','Scenario',930,115,480,75)
if __name__=='__main__':
 if not ANALYSIS.exists():raise SystemExit('Waiting for validated outputs/analysis.json; no substitute data will be generated.')
 data=json.loads(ANALYSIS.read_text())
 for co in ['PG','TRV']:build(co,data[co])
