import fs from 'node:fs/promises';
export async function extendWorkbook(w,R){
 const d=JSON.parse(await fs.readFile(R+'/processed_data/extended_history.json','utf8'));
 const money='$#,##0;($#,##0);"–"',pct='0.0%;(0.0%);"–"';
 const ch=w.worksheets.getItem('PG_2_Analysis'),rev=w.worksheets.getItem('PG_3_Analysis'),mar=w.worksheets.getItem('PG_4_Analysis');
 const bs=w.worksheets.add('Reported Balance'),cf=w.worksheets.add('Reported Cash'),drv=w.worksheets.add('Reported Drivers');
 function base(s,title,end=40){s.showGridLines=false;s.getRange(`A1:J${end}`).format.font={name:'Arial',size:12};s.getRange(`A1:J${end}`).format.rowHeight=22;s.getRange(`A1:A${end}`).format.columnWidth=3;s.getRange(`B1:B${end}`).format.columnWidth=59;s.getRange(`C1:H${end}`).format.columnWidth=17;s.getRange('B2').values=[[title]];s.getRange('B2').format.font={name:'Arial',size:18,bold:true,color:'#003DA5'};s.getRange('B3:F3').format.borders={bottom:{style:'thin',color:'#003DA5'}};s.tabColor=s.name.startsWith('PG_')?'#003DA5':'#DFC9A3';}
 function header(s,r,values){const end=String.fromCharCode(65+values.length);s.getRange(`B${r}:${end}${r}`).values=[values];s.getRange(`B${r}:${end}${r}`).format={fill:'#003DA5',font:{name:'Arial',size:12,bold:true,color:'#FFFFFF'},rowHeight:26};}
 function val(s,c,v){s.getRange(c).values=[[v]];}function form(s,c,v){s.getRange(c).formulas=[[v]];}
 function red(s,range){s.getRange(range).format.font.color='#C00000';s.getRange(range).format.font.bold=true;}
 const maps={};
 for(const [s,rows,years,title,page] of [[bs,d.balance_sheet,[2025,2026],'P&G | Reported balance sheet',38],[cf,d.cash_flow,[2024,2025,2026],'P&G | Reported cash flow statement',40]]){
  base(s,title,46);val(s,'B4',`USD millions; ${s===bs?'as of':'fiscal years ended'} 30 June`);header(s,6,['Reported metric',...years.map(y=>'FY'+y)]);maps[s.name]={};
  const short={33:'Convertible Class A preferred stock',34:'Non-voting Class B preferred stock',35:'Common stock',39:s===bs?'Treasury stock':'Cash payments for interest'};
  const cfshort={5:'Cash and restricted cash, beginning of year',26:'Short-term debt additions (>3 months)',27:'Short-term debt reductions (>3 months)',28:'Other short-term debt, net',34:'Exchange-rate effect on cash',35:'Change in cash and restricted cash',36:'Cash and restricted cash, end of year',12:'Intangible impairment charge'};
  rows.forEach((v,i)=>{let row=i+7;maps[s.name][v.source_row]=row;let label=(s===bs?short:cfshort)[v.source_row]||v.metric;val(s,'B'+row,label);s.getRangeByIndexes(row-1,2,1,years.length).values=[v.values];});
  s.getRange(`C7:${s===bs?'D':'E'}${rows.length+6}`).setNumberFormat(money);
  s.getRange(`B7:B${rows.length+6}`).format.font.size=11;
  val(s,'B'+(rows.length+8),`Source: P&G 2026 Annual Report, printed p.${page}. Original amounts retained.`);
  val(s,'B'+(rows.length+9),s===bs?'FY2024 balance sheet is not included in this source.':'Prior operating cash flow rows were reclassified by the company.');
  for(const sr of s===bs?[7,20,31,42]:[7,17,36])red(s,`B${maps[s.name][sr]}:${s===bs?'D':'E'}${maps[s.name][sr]}`);
 }
 base(drv,'P&G | Reported business drivers',43);drv.getRange('C1:H43').format.columnWidth=14;
 val(drv,'B4','Company disclosures; percentages are approximate growth contributions.');
 header(drv,6,['FY2026 vs FY2025','Volume','FX','Price','Mix','Other','Growth']);drv.getRange('B7:H12').values=d.sales_drivers;drv.getRange('C7:H12').setNumberFormat('0%');red(drv,'B12:H12');
 header(drv,15,['Segment sales (USD millions)','FY2025','FY2026']);drv.getRange('B16:D21').values=d.segments;drv.getRange('C16:D21').setNumberFormat(money);red(drv,'B16:D16');
 header(drv,24,['Gross margin driver','Effect (bps)']);drv.getRange('B25:C33').values=d.gross_margin_drivers;drv.getRange('C25:C33').setNumberFormat('0;[Red](0);"–"');red(drv,'B25:C27');red(drv,'B32:C33');
 val(drv,'B35','Sources: Annual Report pp.20–22 (drivers) and pp.44–45 (segment sales).');
 val(drv,'B36','Organic sales growth: 1%. Driver percentages must not be treated as exact dollar effects.');
 val(drv,'B37','Reported gross margin: 51.2% in FY2025; 50.2% in FY2026 (−100 bps).');
 val(drv,'B38','Reported SG&A ratio: 26.9% to 27.5%; operating margin: 24.3% to 22.7%.');
 base(ch,'P&G | Three-statement checks',38);val(ch,'B4','Difference = calculated amount less reported amount; USD millions.');header(ch,6,['Check','FY2024','FY2025','FY2026']);
 const ref=(name,col,sr)=>`'${name}'!${col}${maps[name][sr]}`;
 const checks=[['Operating income: sales less operating costs',c=>`'Reported Earnings'!${c}7-SUM('Reported Earnings'!${c}8:${c}10)-'Reported Earnings'!${c}11`],['Earnings before tax',c=>`SUM('Reported Earnings'!${c}11:${c}14)-'Reported Earnings'!${c}15`],['Net earnings: earnings before tax less tax',c=>`'Reported Earnings'!${c}15-'Reported Earnings'!${c}16-'Reported Earnings'!${c}17`],['Net earnings: income statement less cash flow',c=>`'Reported Earnings'!${c}17-${ref('Reported Cash',c,7)}`],['Operating cash flow: components less total',c=>`${d.cash_flow.filter(x=>x.source_row>=7&&x.source_row<=16).map(x=>ref('Reported Cash',c,x.source_row)).join('+')}-${ref('Reported Cash',c,17)}`],['Investing cash flow: components less total',c=>`${[19,20,21,22].map(r=>ref('Reported Cash',c,r)).join('+')}-${ref('Reported Cash',c,23)}`],['Financing cash flow: components less total',c=>`${[25,26,27,28,29,30,31,32].map(r=>ref('Reported Cash',c,r)).join('+')}-${ref('Reported Cash',c,33)}`],['Cash change: flows plus FX less reported change',c=>`${[17,23,33,34].map(r=>ref('Reported Cash',c,r)).join('+')}-${ref('Reported Cash',c,35)}`],['Cash roll-forward: opening plus change less close',c=>`${ref('Reported Cash',c,5)}+${ref('Reported Cash',c,35)}-${ref('Reported Cash',c,36)}`]];
 checks.forEach(([label,fn],i)=>{val(ch,'B'+(7+i),label);for(const c of ['C','D','E'])form(ch,c+(7+i),'='+fn(c));});
 val(ch,'B17','Assets less reported liabilities and equity');val(ch,'B18','Liabilities plus equity less assets');val(ch,'B19','Cash flow ending cash less balance sheet cash');
 for(const r of [17,18,19])val(ch,'C'+r,'n.a.');
 for(const [c,b] of [['D','C'],['E','D']]){form(ch,c+'17',`=${ref('Reported Balance',b,20)}-${ref('Reported Balance',b,43)}`);form(ch,c+'18',`=${ref('Reported Balance',b,31)}+${ref('Reported Balance',b,42)}-${ref('Reported Balance',b,20)}`);form(ch,c+'19',`=${ref('Reported Cash',c,36)}-${ref('Reported Balance',b,7)}`);}
 ch.getRange('C7:E19').setNumberFormat('0.00;(0.00);0.00');
 ch.getRange('C7:E19').conditionalFormats.add('expression',{formula:'AND(ISNUMBER(C7),ABS(C7)>1)',format:{fill:'#FCE4D6',font:{color:'#C00000',bold:true}}});
 val(ch,'B21','0.00 = exact agreement; ±1.00 = retained source rounding residual.');val(ch,'B22','A residual within $1m is reviewed, not rewritten or presented as an exact tie.');val(ch,'B23','FY2024 balance-sheet checks: n.a. because this report shows only FY2025–FY2026.');
 header(ch,25,['FY2026 cross-statement evidence','Amount']);val(ch,'B26','Net earnings in income statement');form(ch,'C26',"='Reported Earnings'!E17");val(ch,'B27','Net earnings in cash flow');form(ch,'C27','='+ref('Reported Cash','E',7));val(ch,'B28','Ending cash in cash flow');form(ch,'C28','='+ref('Reported Cash','E',36));val(ch,'B29','Cash in balance sheet');form(ch,'C29','='+ref('Reported Balance','D',7));ch.getRange('C26:C29').setNumberFormat(money);red(ch,'B26:C29');val(ch,'B31','Source: reported statement sheets; Annual Report pp.37, 38 and 40.');
 base(rev,'P&G | Revenue drivers',35);val(rev,'B4','FY2026 vs FY2025. Exact segment dollar changes; approximate company drivers.');header(rev,6,['Segment','FY2025','FY2026','Change ($m)','Share of change']);
 for(let i=0;i<6;i++){let r=7+i;form(rev,'B'+r,`='Reported Drivers'!B${16+i}`);form(rev,'C'+r,`='Reported Drivers'!C${16+i}`);form(rev,'D'+r,`='Reported Drivers'!D${16+i}`);form(rev,'E'+r,`=D${r}-C${r}`);form(rev,'F'+r,`=E${r}/$E$14`);}
 val(rev,'B14','Consolidated revenue');form(rev,'C14',"='Reported Earnings'!D7");form(rev,'D14',"='Reported Earnings'!E7");form(rev,'E14','=D14-C14');form(rev,'F14','=SUM(F7:F12)');rev.getRange('C7:E14').setNumberFormat(money);rev.getRange('F7:F14').setNumberFormat(pct);red(rev,'B7:F7');
 val(rev,'B16','Segment totals less consolidated sales');form(rev,'C16','=SUM(C7:C12)-C14');form(rev,'D16','=SUM(D7:D12)-D14');form(rev,'E16','=SUM(E7:E12)-E14');rev.getRange('C16:E16').setNumberFormat('0.00;(0.00);0.00');
 header(rev,19,['Total-company driver','Contribution']);for(const [i,l] of ['Volume','Foreign exchange','Price','Mix','Other'].entries()){val(rev,'B'+(20+i),l);form(rev,'C'+(20+i),`='Reported Drivers'!${String.fromCharCode(67+i)}12`);}
 val(rev,'B25','Sum of approximate contributions');form(rev,'C25','=SUM(C20:C24)');val(rev,'B26','Growth from reported dollar values');form(rev,'C26','=D14/C14-1');rev.getRange('C20:C26').setNumberFormat(pct);red(rev,'B21:C22');
 val(rev,'B28','Beauty contributes the largest dollar increase; exact contribution uses segment changes.');val(rev,'B29','Driver percentages are rounded company disclosures, not an exact dollar bridge.');val(rev,'B30','Source: Annual Report pp.20, 22, 44–45; segment totals retain $1m rounding residuals.');
 base(mar,'P&G | Profit margin drivers',37);val(mar,'B4','FY2026 vs FY2025. Calculated margins and company explanations are shown separately.');header(mar,6,['Calculated metric','FY2025','FY2026','Change (bps)']);
 for(const [r,l,num] of [[7,'Gross margin',9],[8,'SG&A / sales',10],[9,'Operating margin',12]]){val(mar,'B'+r,l);for(const [c,source] of [['C','D'],['D','E']])form(mar,c+r,`='PG_1_Analysis'!${source}${num}/'PG_1_Analysis'!${source}7`);form(mar,'E'+r,`=(D${r}-C${r})*10000`);}
 mar.getRange('C7:D9').setNumberFormat(pct);mar.getRange('E7:E9').setNumberFormat('0.0;(0.0);"–"');red(mar,'B7:E9');header(mar,12,['Company gross margin explanation','Effect (bps)']);
 for(let i=0;i<9;i++){form(mar,'B'+(13+i),`='Reported Drivers'!B${25+i}`);form(mar,'C'+(13+i),`='Reported Drivers'!C${25+i}`);}
 val(mar,'B22','Total explained gross margin change');form(mar,'C22','=SUM(C13:C21)');mar.getRange('C13:C22').setNumberFormat('0;(0);"–"');red(mar,'B13:C15');red(mar,'B20:C22');
 val(mar,'B25','Higher SG&A ($m)');form(mar,'C25',"='PG_1_Analysis'!F10");mar.getRange('C25').setNumberFormat(money);val(mar,'B27','Management attributes the SG&A ratio increase primarily to marketing.');val(mar,'B28','The narrative does not provide an exact SG&A driver bridge.');val(mar,'B29','Do not subtract the stated productivity benefit again: it is already included.');val(mar,'B31','Company rounded changes: gross −100 bps; SG&A +60 bps; operating −160 bps.');val(mar,'B32','Calculated margins use reported dollar values; rounding explains the difference.');val(mar,'B34','Source: Annual Report pp.20–21 and 37. One basis point = 0.01 percentage point.');
 w.recalculate();
 const values=ch.getRange('C7:E19').values;for(const row of values)for(const v of row)if(typeof v==='number'&&Math.abs(v)>1)throw Error('Statement check exceeds $1m: '+v);
 if(rev.getRange('E16').values[0][0]!==0||mar.getRange('C22').values[0][0]!==-100)throw Error('Driver reconciliation failed');
 await fs.writeFile(R+'/outputs/extended_checks.json',JSON.stringify({reported_statement_inputs:199,statement_checks:values,source_rounding_tolerance_usd_million:1,segment_growth_check:rev.getRange('E16').values[0][0],gross_margin_bps:mar.getRange('C22').values[0][0],source_row_to_workbook_row:maps},null,2));
 for(const [sheet,range] of [[ch,'B2:F31'],[rev,'B2:F30'],[mar,'B2:F34'],[bs,'B2:E41'],[cf,'B2:F39'],[drv,'B2:H38']]){const im=await w.render({sheetName:sheet.name,range,scale:1.3,format:'png'});await fs.writeFile(R+'/evidence/preview_'+sheet.name+'.png',new Uint8Array(await im.arrayBuffer()));}
}
