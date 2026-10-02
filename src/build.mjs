import fs from 'node:fs/promises';
import path from 'node:path';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
import {extendWorkbook} from './extend_workbook.mjs';
const R=path.resolve(import.meta.dirname,'..');
const data=JSON.parse(await fs.readFile(path.join(R,'processed_data/financial_history.json'),'utf8'));
const w=Workbook.create(),a=w.worksheets.add('PG_1_Analysis');
for(const name of ['PG_2_Analysis','PG_3_Analysis','PG_4_Analysis'])w.worksheets.add(name);
const s=w.worksheets.add('Reported Earnings');
const money='$#,##0;($#,##0);"–"',num='#,##0;(#,##0);"–"',pct='0.0%;(0.0%);"–"';
for(const sh of [a,s]){
 sh.showGridLines=false;sh.getRange('A1:H33').format.font={name:'Arial',size:12};sh.getRange('A1:H33').format.rowHeight=22;
 sh.getRange('A1:A33').format.columnWidth=3;sh.getRange('B1:B33').format.columnWidth=58;sh.getRange('C1:F33').format.columnWidth=17;sh.getRange('G1:H33').format.columnWidth=3;
 sh.getRange('B2').format.font={name:'Arial',size:18,bold:true,color:'#003DA5'};
 sh.getRange('B3:F3').format.borders={bottom:{style:'thin',color:'#003DA5'}};
}
a.tabColor='#003DA5';s.tabColor='#DFC9A3';
function head(sh,r,values){sh.getRange(`B${r}:F${r}`).values=[values];sh.getRange(`B${r}:F${r}`).format={fill:'#003DA5',font:{name:'Arial',size:12,bold:true,color:'#FFFFFF'},rowHeight:26};}
s.getRange('B2').values=[['P&G | Reported income statement']];s.getRange('B4').values=[['Fiscal years ended 30 June; USD millions, except EPS']];
head(s,6,['Reported metric','FY2024','FY2025','FY2026','Classification']);
s.getRange('B7:F21').values=data.map(d=>[d.metric,...d.values,d.type]);s.getRange('C7:E21').setNumberFormat(money);s.getRange('C20:E21').setNumberFormat('$0.00');
const labels={7:'Net sales',8:'Cost of products sold',9:'Selling, general and administrative expense',10:'Intangible asset impairment',11:'Operating income',12:'Interest expense',13:'Interest income',14:'Other non-operating income, net',15:'Earnings before income taxes',16:'Income taxes',17:'Net earnings',18:'Net earnings attributable to noncontrolling interests',19:'Net earnings attributable to P&G',20:'Basic EPS',21:'Diluted EPS'};
for(const [r,l] of Object.entries(labels))s.getRange('B'+r).values=[[l]];
for(const r of [7,11]){s.getRange(`B${r}:E${r}`).format.font.color='#C00000';s.getRange(`B${r}:E${r}`).format.font.bold=true;}
s.getRange('B23').values=[['Source: P&G 2026 Annual Report, printed p.37 (PDF p.49).']];
s.getRange('B24').values=[['Company financial spreadsheet: income statement, rows 5–21.']];
s.getRange('B25').values=[['Source dashes on impairment are recorded as zero; no adjustments made.']];
s.getRange('B26').values=[['Red marks highlight matching evidence, not a positive or negative result.']];
s.getRange('B28').values=[['https://s204.q4cdn.com/332108499/files/doc_financials/2026/ar/2026_annual_report.pdf']];s.getRange('B28').format.font.size=9;
a.getRange('B2').values=[['P&G | Revenue growth and operating profit']];a.getRange('B4').values=[['FY2026 sales grew; operating profit declined. Amounts in USD millions.']];
head(a,6,['Metric','FY2024','FY2025','FY2026','FY26 vs FY25']);
const defs=[['Net sales',7],['Cost of products sold',8],['Gross profit',null],['SG&A',9],['Intangible impairment',10],['Operating income',11]];
defs.forEach(([label,sr],i)=>{let r=7+i;a.getRange('B'+r).values=[[label]];for(const c of ['C','D','E']){a.getRange(c+r).formulas=[[sr?`='Reported Earnings'!${c}${sr}`:`=${c}7-${c}8`]];}a.getRange('F'+r).formulas=[[`=E${r}-D${r}`]];});a.getRange('C7:F12').setNumberFormat(money);
for(const [r,label,numerator] of [[14,'Gross margin',9],[15,'Operating margin',12]]){a.getRange('B'+r).values=[[label]];for(const c of ['C','D','E'])a.getRange(c+r).formulas=[[`=${c}${numerator}/${c}7`]];a.getRange('F'+r).formulas=[[`=(E${r}-D${r})*10000`]];a.getRange(`C${r}:E${r}`).setNumberFormat(pct);a.getRange('F'+r).setNumberFormat('0.0" bps";(0.0)" bps";"–"');}
a.getRange('B17').values=[['FY2026 growth vs FY2025']];a.getRange('C17').values=[['Revenue']];a.getRange('D17').formulas=[['=E7/D7-1']];a.getRange('E17').values=[['Operating profit']];a.getRange('F17').formulas=[['=E12/D12-1']];a.getRange('D17').setNumberFormat(pct);a.getRange('F17').setNumberFormat(pct);
head(a,19,['Operating profit bridge','Effect (USD m)','','','']);
const bridge=[['Revenue increase','=F7'],['Higher cost of products sold','=-F8'],['Higher SG&A','=-F10'],['Change in impairment','=-F11'],['Net operating profit change','=SUM(C20:C23)']];
bridge.forEach(([l,f],i)=>{a.getRange('B'+(20+i)).values=[[l]];a.getRange('C'+(20+i)).formulas=[[f]];});a.getRange('C20:C24').setNumberFormat(money);
a.getRange('B26').values=[['Bridge less reported operating profit change']];a.getRange('C26').formulas=[['=C24-F12']];a.getRange('C26').setNumberFormat('0.00');
a.getRange('B28').values=[['Reported: source financial amounts. Derived: gross profit, margins and changes.']];
a.getRange('B29').values=[['FY2024 includes $1,341m impairment; the FY2025 recovery is not fully recurring.']];
a.getRange('B30').values=[['Gross profit uses net sales less cost of products sold; no adjusted series created.']];
for(const r of [7,12]){a.getRange(`B${r}:F${r}`).format.font.color='#C00000';a.getRange(`B${r}:F${r}`).format.font.bold=true;}
for(const sh of [a,s])sh.getRange('B23:F30').format.rowHeight=22;
await extendWorkbook(w,R);
w.recalculate();
const checks={revenue_change:a.getRange('F7').values[0][0],operating_profit_change:a.getRange('F12').values[0][0],bridge_check:a.getRange('C26').values[0][0],revenue_growth:a.getRange('D17').values[0][0],operating_growth:a.getRange('F17').values[0][0]};
if(checks.revenue_change!==2748||checks.operating_profit_change!==-703||checks.bridge_check!==0)throw Error(JSON.stringify(checks));
let before=a.getRange('E9').values[0][0];s.getRange('E7').values=[[87042]];w.recalculate();if(a.getRange('E9').values[0][0]!==before+10)throw Error('Formula propagation failed');s.getRange('E7').values=[[87032]];w.recalculate();
const errors=await w.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!',options:{useRegex:true,maxResults:30}});
await fs.writeFile(path.join(R,'outputs/calculation_checks.json'),JSON.stringify({checks,formula_scan:errors,propagation_test:'Revenue input +10 changes derived gross profit +10; input restored.'},null,2));
for(const sh of [a,s]){let im=await w.render({sheetName:sh.name,range:sh===a?'B2:F30':'B2:F28',scale:1.5,format:'png'});await fs.writeFile(path.join(R,'evidence',sh===a?'analysis_preview.png':'reported_preview.png'),new Uint8Array(await im.arrayBuffer()));}
await (await SpreadsheetFile.exportXlsx(w)).save(path.join(R,'outputs/PG_1_Analysis.xlsx'));console.log(checks);
