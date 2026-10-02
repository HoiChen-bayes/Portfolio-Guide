"""Download latest published actuals, outside the isolated forecast packet."""
import urllib.request,json,hashlib
from pathlib import Path
from html.parser import HTMLParser
class Parser(HTMLParser):
 def __init__(self):
  super().__init__();self.tables=[];self.table=None;self.row=None;self.cell=None;self.text=[]
 def handle_starttag(self,t,a):
  if t=='table':self.table=[]
  elif t=='tr' and self.table is not None:self.row=[]
  elif t in ['td','th'] and self.row is not None:self.cell=[]
 def handle_data(self,d):
  self.text.append(d)
  if self.cell is not None:self.cell.append(d)
 def handle_endtag(self,t):
  if t in ['td','th'] and self.cell is not None:self.row.append(' '.join(' '.join(self.cell).split()));self.cell=None
  elif t=='tr' and self.row is not None:self.table.append(self.row);self.row=None
  elif t=='table' and self.table is not None:self.tables.append(self.table);self.table=None
def main():
 p=Path(__file__).resolve().parents[1]/'data/holdout';p.mkdir(exist_ok=True)
 urls={'PG':'https://us.pg.com/newsroom/news-releases/PG-Announces-Fourth-Quarter-and-Fiscal-Year-2026-Results/','TRV':'https://investor.travelers.com/newsroom/press-releases/news-details/2026/Travelers-Reports-Excellent-Second-Quarter-and-Year-to-Date-Results/default.aspx'}
 manifest=[]
 for c,u in urls.items():
  b=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'})).read();(p/f'{c}.html').write_bytes(b)
  s=Parser();s.feed(b.decode());(p/f'{c}.txt').write_text(' '.join(s.text));(p/f'{c}_tables.json').write_text(json.dumps(s.tables,indent=2))
  manifest.append(dict(company=c,url=u,published_at='2026-07-29' if c=='PG' else '2026-07-17',sha256=hashlib.sha256(b).hexdigest()));print(c,len(s.tables))
 (p/'manifest.json').write_text(json.dumps(manifest,indent=2))
if __name__=='__main__':main()
