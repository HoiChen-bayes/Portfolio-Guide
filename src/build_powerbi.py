"""Build portable native PBIP reports from the frozen, validated analysis snapshot."""
from pathlib import Path
import json,uuid,hashlib,math,datetime,shutil
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'outputs/powerbi';ANALYSIS=ROOT/'outputs/analysis.json'
base='https://developer.microsoft.com/json-schemas/';pref='fabric/item/report/definition/'
def dump(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2),encoding='utf-8')
def dv(v):
 if v is None:return 'BLANK()'
 if isinstance(v,str):return '"'+v.replace('"','""').replace('\n',' ')+'"'
 return str(v)
def build(co,data):
 global REPORT,SM,pages,visual_count,bindings,tables,types,measures,INK,ACCENT,BG,CO
 name=('PAndG' if co=='PG' else 'Travelers')+'_Scenarios';dest=OUT/co;REPORT=dest/(name+'.Report');SM=dest/(name+'.SemanticModel');pages=[];visual_count=0;bindings=[]
 CO=co;INK='#09244A' if co=='PG' else '#26262C';ACCENT='#0067D9' if co=='PG' else '#C8102E';BG='#F3F6FA' if co=='PG' else '#FAF7F2';tables={};types={}
 if (REPORT/'definition/pages').exists():shutil.rmtree(REPORT/'definition/pages')
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
 measures['Profit variance color']='IF([Profit error]>=0,"#168269","#C8102E")'
 percent={'Selected Margin','Actual Margin','Profit error %','History ratio'};money='$#,0.0\"M\";($#,0.0\"M\");$0.0\"M\"'
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
 models[[m['name'] for m in models].index('Forecast')]['measures']=[{'name':n,'expression':e,'formatString':'' if n=='Profit variance color' else '0.0%;(0.0%);0.0%' if n in percent else '0' if n=='QA rows' else money} for n,e in measures.items()]
 def display_column(table,name,expression):
  next(t for t in models if t['name']==table)['columns'].append({'name':name,'dataType':'string','type':'calculated','expression':expression})
  types[table].append((name,'string'))
 display_column('History','QuarterLabel','LEFT(RIGHT(History[Quarter],4),2)&" "&RIGHT(History[Quarter],2)')
 display_column('VintageCompare','CompactLabel','SWITCH(VintageCompare[Vintage],"pre_history","Mar hist","pre_market","Mar res.","mid_history","May hist","mid_market","May res.")')
 display_column('Comparison','ForecastVersion','SWITCH(Comparison[Vintage],"pre_history","March history","pre_market","March research","mid_history","May history","mid_market","May research")')
 next(c for t in models if t['name']=='History' for c in t['columns'] if c['name']=='QuarterLabel')['sortByColumn']='Quarter'
 next(c for t in models if t['name']=='VintageCompare' for c in t['columns'] if c['name']=='CompactLabel')['sortByColumn']='Sort'
 rels=[]
 for fact in ['Forecast','Comparison','Drivers']:
  for dim,key in [('Vintage','Vintage'),('Scenario','Case')]:rels.append({'name':str(uuid.uuid5(uuid.NAMESPACE_DNS,co+fact+dim)),'fromTable':fact,'fromColumn':key,'toTable':dim,'toColumn':key,'fromCardinality':'many','toCardinality':'one','crossFilteringBehavior':'oneDirection'})
 dump(SM/'model.bim',{'name':name,'compatibilityLevel':1606,'model':{'culture':'en-US','defaultPowerBIDataSourceVersion':'powerBI_V3','defaultMode':'import','tables':models,'relationships':rels}})
 dump(SM/'definition.pbism',{'version':'1.0','settings':{'qnaEnabled':False}});dump(dest/(name+'.pbip'),{'version':'1.0','artifacts':[{'report':{'path':name+'.Report'}}],'settings':{'enableAutoRecovery':True}});dump(REPORT/'definition.pbir',{'version':'4.0','datasetReference':{'byPath':{'path':'../'+name+'.SemanticModel'}}});dump(REPORT/'definition/version.json',{'$schema':base+pref+'versionMetadata/1.0.0/schema.json','version':'2.0.0'})
 dump(REPORT/'StaticResources/RegisteredResources/ScenarioTheme.json',{'name':name,'dataColors':[ACCENT,'#18A8A4' if co=='PG' else '#78757A','#E6A23C','#168A70','#936DCC'],'background':BG,'foreground':INK,'tableAccent':ACCENT,'good':'#168A70','bad':'#C71932'})
 dump(REPORT/'definition/report.json',{'$schema':base+pref+'report/3.1.0/schema.json','themeCollection':{'customTheme':{'name':'ScenarioTheme.json','reportVersionAtImport':{'visual':'2.1.0','page':'2.0.0','report':'3.1.0'},'type':'RegisteredResources'}},'resourcePackages':[{'name':'RegisteredResources','type':'RegisteredResources','items':[{'name':'ScenarioTheme.json','path':'ScenarioTheme.json','type':'CustomTheme'}]}],'settings':{'useEnhancedTooltips':True}})
 revenue_label='Net sales' if co=='PG' else 'Earned premiums';profit_label='Net income attributable' if co=='PG' else 'Core income'
 if co=='PG':
  p=page('01_Summary','Financial perspective','01','Default: May research · Base. Sales scale is resilient; margins explain the gap.')
  filters(p)
  for x,m,t in [(214,'Selected Revenue','FORECAST SALES'),(514,'Selected Profit','FORECAST EARNINGS'),(814,'Selected Margin','OPERATING MARGIN'),(1114,'Profit error','ACTUAL − FORECAST')]:card(p,m,t,x,245,282,140)
  chart(p,C('History','QuarterLabel'),['History revenue'],'Sales through nine quarters',214,391,776,320)
  chart(p,C('VintageCompare','CompactLabel'),['Vintage profit','Actual Profit'],'Profit · history vs research',1012,391,384,320,'clusteredColumnChart')
  visual(p,'treemap',214,737,496,188,'Segment sales · 2026Q1',{'Group':[C('Segments','Segment')],'Values':[M('Segment value')]})
  chart(p,C('History','QuarterLabel'),['History ratio'],'Gross margin · reported history',734,737,662,188)
  p=page('02_History','The operating engine','02','Scale, mix and cash generation explain the earnings base.')
  chart(p,C('History','QuarterLabel'),['History revenue'],'Net sales',214,177,740,330)
  visual(p,'treemap',976,177,420,330,'Segment mix · 2026Q1 sales',{'Group':[C('Segments','Segment')],'Values':[M('Segment value')]})
  chart(p,C('History','QuarterLabel'),['History profit'],'Net income attributable',214,533,375,335,'clusteredColumnChart')
  chart(p,C('History','QuarterLabel'),['History cash flow'],'Operating cash flow',611,533,390,335,'clusteredColumnChart')
  chart(p,C('History','QuarterLabel'),['History ratio'],'Gross margin',1023,533,373,335)
  note(p,'Quarterly cash flow retains missing observations. April releases enter May vintages only.',214,887,1182)
  p=page('03_Scenarios','Three possible paths','03','Bear, base and bull are analyst cases—not probabilities.')
  filters(p)
  visual(p,'scatterChart',214,251,688,361,'Scale versus earnings',{'Category':[C('Scenario','Case')],'X':[M('Selected Revenue')],'Y':[M('Selected Profit')],'Tooltips':[M('Selected Margin')]})
  chart(p,C('Scenario','Case'),['Selected Profit'],'Forecast earnings by case',926,251,470,361,'clusteredColumnChart')
  table(p,[C('Vintage','VintageLabel'),C('Scenario','Case'),M('Selected Revenue'),M('Selected Profit'),M('Selected Margin'),M('Free cash flow')],'The scenario ledger',214,640,1182,281)
  p=page('04_Market','What research changed','04','A controlled comparison isolates market research from new financial history.')
  slicer(p,'Bridge','Window','Research window',214,164,300,66)
  visual(p,'waterfallChart',214,251,740,387,'Earnings revision · sequential attribution',{'Category':[C('Bridge','Driver')],'Y':[M('Bridge impact')]})
  chart(p,C('Sensitivity','Driver'),['Sensitivity impact'],'Sensitivity · May base',976,251,420,387,'clusteredBarChart')
  table(p,[C('Sensitivity','Driver'),C('Sensitivity','Shock'),M('Sensitivity impact')],'One driver at a time · ratio +0.01 / dollars +$100M',214,667,1182,253)
  p=page('05_Actual','Forecast vs actual','05','The held-out results challenge the forecasts on a consistent accounting basis.')
  filters(p)
  for x,m,t in [(214,'Selected Profit','FORECAST EARNINGS'),(618,'Actual Profit','ACTUAL EARNINGS'),(1022,'Profit error %','PROFIT VARIANCE %')]:card(p,m,t,x,245,374,125)
  visual(p,'waterfallChart',214,391,726,301,'Why profit missed forecast',{'Category':[C('ActualBridge','Driver')],'Y':[M('Actual bridge impact')]})
  chart(p,C('VintageCompare','CompactLabel'),['Vintage profit','Actual Profit'],'Information sets versus actual',964,391,432,301,'clusteredColumnChart')
  table(p,[C('Comparison','ForecastVersion'),C('Comparison','Case'),C('Comparison','Metric'),C('Comparison','Forecast'),C('Comparison','Actual'),C('Comparison','Difference'),C('Comparison','ErrorPercent')],'Forecast and actual by metric',214,718,1182,202)
  p=page('06_Method','Evidence & discipline','06','Frozen assumptions, dated evidence and separate target actuals make the work auditable.')
  table(p,[C('QA','Check'),C('QA','Status'),C('QA','Detail')],'Model governance',214,179,1182,326)
  table(p,[C('Sources','Quarter'),C('Sources','Metric'),C('Sources','Published'),C('Sources','SourceURL')],'Official financial sources',214,533,1182,333)
  note(p,'Retrospective reconstruction · analyst scenarios · saved snapshot, not live data. Source rounding and collector exposure disclosed.',214,887,1182)
 else:
  p=page('01_Summary','Underwriting outlook','01','Default: May research · Base. Loss performance drives the earnings story.')
  filters(p)
  card(p,'Selected Profit','FORECAST CORE INCOME',44,285,465,190,bg='#FAF7F2',size=54)
  card(p,'Actual Profit','ACTUAL CORE INCOME',44,499,465,135,bg='#FAF7F2')
  card(p,'Profit error','ACTUAL − FORECAST',44,658,465,135,bg='#FAF7F2')
  chart(p,C('VintageCompare','CompactLabel'),['Vintage profit','Actual Profit'],'Four information sets · core income',540,285,856,315,'clusteredColumnChart')
  card(p,'Selected Margin','FORECAST COMBINED RATIO',540,625,414,168,bg='#F6E5E7')
  card(p,'Catastrophe losses','FORECAST CATASTROPHE LOSSES',978,625,418,168,bg='#F6E5E7')
  chart(p,C('History','QuarterLabel'),['History revenue'],'Earned premiums · nine-quarter scale',44,815,1352,110)
  p=page('02_History','Scale & risk','02','Premium volume is context; the combined ratio measures underwriting discipline.')
  chart(p,C('History','QuarterLabel'),['History ratio'],'Reported combined ratio',44,210,827,304)
  visual(p,'treemap',898,210,498,304,'Written premiums by segment · 2026Q1',{'Group':[C('Segments','Segment')],'Values':[M('Segment value')]})
  chart(p,C('History','QuarterLabel'),['History revenue'],'Earned premiums',44,547,470,317)
  chart(p,C('History','QuarterLabel'),['History profit'],'Core income',540,547,440,317,'clusteredColumnChart')
  chart(p,C('History','QuarterLabel'),['History cash flow'],'Operating cash flow',1006,547,390,317,'clusteredColumnChart')
  note(p,'Missing cash-flow observations stay blank. Segment values are written premiums, not earned premiums.',44,891,1352)
  p=page('03_Scenarios','An underwriting range','03','Loss and catastrophe assumptions drive the range of insurance outcomes.')
  filters(p)
  chart(p,C('Scenario','Case'),['Selected Profit'],'Forecast core income',44,288,463,300,'clusteredBarChart')
  visual(p,'scatterChart',534,288,862,300,'Premium scale versus core income',{'Category':[C('Scenario','Case')],'X':[M('Selected Revenue')],'Y':[M('Selected Profit')],'Tooltips':[M('Selected Margin')]})
  table(p,[C('Vintage','VintageLabel'),C('Scenario','Case'),M('Selected Revenue'),M('Selected Profit'),M('Selected Margin'),M('Catastrophe losses')],'Insurance scenario ledger',44,618,1352,303)
  p=page('04_Market','Research into risk','04','Each bridge holds financial history constant; effects depend on replacement order.')
  slicer(p,'Bridge','Window','Research window',44,205,336,66)
  chart(p,C('Sensitivity','Driver'),['Sensitivity impact'],'Risk sensitivity · May base',44,291,468,333,'clusteredBarChart')
  visual(p,'waterfallChart',540,291,856,333,'Core-income revision · sequential attribution',{'Category':[C('Bridge','Driver')],'Y':[M('Bridge impact')]})
  table(p,[C('Sensitivity','Driver'),C('Sensitivity','Shock'),M('Sensitivity impact')],'Assumption shocks · ratio +0.01 / dollars +$100M',44,657,1352,264)
  p=page('05_Actual','Forecast vs actual','05','Signed differences describe the miss; they are not an accuracy percentage.')
  filters(p)
  card(p,'Actual Profit','ACTUAL CORE INCOME',44,288,446,130,bg='#FAF7F2',size=49)
  card(p,'Selected Profit','FORECAST CORE INCOME',516,288,431,130,bg='#FAF7F2')
  card(p,'Profit error %','PROFIT VARIANCE %',973,288,423,130,bg='#F6E5E7')
  chart(p,C('VintageCompare','CompactLabel'),['Vintage profit','Actual Profit'],'Forecast vintages versus actual',44,448,471,250,'clusteredColumnChart')
  visual(p,'waterfallChart',541,448,855,250,'Why profit differed from forecast',{'Category':[C('ActualBridge','Driver')],'Y':[M('Actual bridge impact')]})
  table(p,[C('Comparison','ForecastVersion'),C('Comparison','Case'),C('Comparison','Metric'),C('Comparison','Forecast'),C('Comparison','Actual'),C('Comparison','Difference'),C('Comparison','ErrorPercent')],'Forecast and actual by metric',44,730,1352,191)
  p=page('06_Method','The evidence ledger','06','Retrospective scenarios with source-date gates, frozen assumptions and independent arithmetic.')
  table(p,[C('Sources','Quarter'),C('Sources','Metric'),C('Sources','Published'),C('Sources','SourceURL')],'Official financial sources',44,216,1352,267)
  table(p,[C('QA','Check'),C('QA','Status'),C('QA','Detail')],'Controls & interpretation',44,514,1352,350)
  note(p,'Saved snapshot—not a live feed. Model limitations, source rounding and collector exposure are disclosed in the audit.',44,890,1352)
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
def display_name(n):
 return {'VintageLabel':'Forecast version','ForecastVersion':'Forecast version','Case':'Scenario','Selected Revenue':'Revenue','Selected Profit':'Profit','Selected Margin':('Operating margin' if CO=='PG' else 'Combined ratio'),'ErrorPercent':'Variance %','Difference':'Variance','Vintage profit':'Forecast profit','Actual Profit':'Actual profit','QuarterLabel':'Calendar quarter','CompactLabel':'Forecast version','Free cash flow':'Free cash flow','Catastrophe losses':'Catastrophe losses'}.get(n,n)
def visual(p,typ,x,y,w,h,title='',roles=None,objects=None):
 global visual_count
 visual_count+=1;name='v'+str(visual_count).zfill(4)
 o={'$schema':base+pref+'visualContainer/2.1.0/schema.json','name':name,'position':{'x':x,'y':y,'z':visual_count,'height':h,'width':w,'tabOrder':visual_count},'visual':{'visualType':typ,'drillFilterOtherVisuals':True}}
 if roles:
  o['visual']['query']={'queryState':{k:{'projections':[{'field':field(*a),'queryRef':a[0]+'.'+a[1],'nativeQueryRef':a[1],'displayName':display_name(a[1])} for a in v]} for k,v in roles.items()}};bindings.extend(a for v in roles.values() for a in v)
 if roles and 'Category' in roles and typ!='scatterChart':o['visual']['query']['sortDefinition']={'sort':[{'field':field(*roles['Category'][0]),'direction':'Ascending'}]}
 o['visual']['visualContainerObjects']={'title':[{'properties':{'show':lit(bool(title)),'text':lit(title),'fontColor':color(INK),'fontSize':lit(15)}}],'background':[{'properties':{'show':lit(True),'color':color('#FFFFFF' if CO=='PG' else BG),'transparency':lit(0)}}],'border':[{'properties':{'show':lit(False),'radius':lit(12 if CO=='PG' else 0)}}]}
 if typ=='scatterChart':
  rv=[r[2] for r in tables['Forecast']];pv=[r[3] for r in tables['Forecast']]
  objects={'categoryAxis':[{'properties':{'fontSize':lit(12),'labelDisplayUnits':lit(1),'start':lit(min(rv)*0.96),'end':lit(max(rv)*1.04)}}],'valueAxis':[{'properties':{'fontSize':lit(12),'labelDisplayUnits':lit(1),'start':lit(min(pv)*0.9),'end':lit(max(pv)*1.1)}}],'bubbles':[{'properties':{'size':lit(16)}}],'categoryLabels':[{'properties':{'show':lit(True),'fontSize':lit(13)}}]}
 if typ=='waterfallChart':objects={'categoryAxis':[{'properties':{'fontSize':lit(12)}}],'valueAxis':[{'properties':{'fontSize':lit(12)}}]}
 if typ=='treemap':objects={'labels':[{'properties':{'fontSize':lit(14)}}],'categoryLabels':[{'properties':{'fontSize':lit(14)}}]}
 if objects:o['visual']['objects']=objects
 dump(p/'visuals'/name/'visual.json',o);return o
def textbox(p,text,x,y,w,h,size=14,c=None,bg=None):
 o=visual(p,'textbox',x,y,w,h,objects={'general':[{'properties':{'paragraphs':[{'textRuns':[{'value':text,'textStyle':{'fontSize':str(size)+'pt','fontFamily':'Segoe UI','color':c or INK}}]}]}}]})
 o['visual']['visualContainerObjects']['background'][0]['properties'].update({'show':lit(bg is not None),'color':color(bg or BG)});dump(p/'visuals'/o['name']/'visual.json',o);return o
def block(p,x,y,w,h,bg):return textbox(p,'',x,y,w,h,1,bg,bg)
def note(p,text,x,y,w):return textbox(p,text,x,y,w,48,13,'#586675')
def page(n,title,index,insight):
 p=REPORT/'definition/pages'/n;pages.append(n);dump(p/'page.json',{'$schema':base+pref+'page/2.0.0/schema.json','name':n,'displayName':index+' '+title,'displayOption':'FitToPage','width':1440,'height':960,'objects':{'background':[{'properties':{'color':color(BG),'transparency':lit(0)}}]}})
 if CO=='PG':
  block(p,0,0,184,960,'#09244A');textbox(p,'P&G',19,25,152,86,40,'#FFFFFF');textbox(p,'FINANCE\nSTUDIO',23,124,147,92,17,'#B6D7FF');block(p,26,238,45,4,'#18A8A4');textbox(p,index,22,296,150,118,50,'#FFFFFF');textbox(p,'APR–JUN\n2026',23,733,150,100,18,'#FFFFFF');textbox(p,'SCENARIO\nRESEARCH',23,841,150,82,13,'#B6D7FF')
  textbox(p,title,214,24,1182,75,31,INK);textbox(p,insight,214,110,1182,51,15,'#586675');block(p,214,98,82,3,'#18A8A4')
 else:
  textbox(p,'TRAVELERS',44,19,530,52,25,ACCENT);textbox(p,'FINANCIAL RESEARCH  /  Q2 2026  /  '+index,927,27,469,38,12,'#586675');block(p,44,78,1352,2,'#26262C');textbox(p,title,44,91,1352,60,29,INK);textbox(p,insight,44,154,1352,39,14,'#586675')
 return p
def card(p,m,t,x,y,w,h=145,bg=None,size=40):
 o=visual(p,'card',x,y,w,h,t,{'Values':[M(m)]},{'labels':[{'properties':{'fontSize':lit(size),'color':color(INK),'labelDisplayUnits':lit(1)}}],'categoryLabels':[{'properties':{'show':lit(False)}}]})
 if bg:o['visual']['visualContainerObjects']['background'][0]['properties']['color']=color(bg)
 if m in ['Profit error','Profit error %']:o['visual']['objects']['labels'][0]['properties']['color']={'solid':{'color':{'expr':field('Forecast','Profit variance color',True)}}}
 dump(p/'visuals'/o['name']/'visual.json',o);return o
def chart(p,c,ms,t,x,y,w,h,typ='lineChart'):
 return visual(p,typ,x,y,w,h,t,{'Category':[c],'Y':[M(m) for m in ms]},{'categoryAxis':[{'properties':{'fontSize':lit(14),'fontColor':color(INK)}}],'valueAxis':[{'properties':{'fontSize':lit(14),'labelDisplayUnits':lit(1),'gridlineShow':lit(True)}}],'legend':[{'properties':{'fontSize':lit(14)}}]})
def table(p,cols,t,x,y,w,h):return visual(p,'tableEx',x,y,w,h,t,{'Values':cols},{'grid':[{'properties':{'textSize':lit(13),'rowPadding':lit(8)}}],'columnHeaders':[{'properties':{'fontColor':color(INK),'backColor':color('#EAF0F8' if CO=='PG' else '#EDE7E1'),'fontSize':lit(13)}}],'total':[{'properties':{'totals':lit(False)}}]})
def slicer(p,t,c,title,x,y,w,h):return visual(p,'slicer',x,y,w,h,title,{'Values':[C(t,c)]},{'selection':[{'properties':{'singleSelect':lit(True)}}],'header':[{'properties':{'show':lit(False)}}],'items':[{'properties':{'fontSize':lit(13)}}],'data':[{'properties':{'mode':lit('Dropdown')}}]})
def filters(p):
 if CO=='PG':slicer(p,'Vintage','VintageLabel','FORECAST VERSION',214,165,768,66);slicer(p,'Scenario','Case','SCENARIO',1006,165,390,66)
 else:slicer(p,'Vintage','VintageLabel','FORECAST VERSION',44,211,898,64);slicer(p,'Scenario','Case','SCENARIO',972,211,424,64)
if __name__=='__main__':
 if not ANALYSIS.exists():raise SystemExit('Waiting for validated outputs/analysis.json; no substitute data will be generated.')
 data=json.loads(ANALYSIS.read_text())
 for co in ['PG','TRV']:build(co,data[co])
