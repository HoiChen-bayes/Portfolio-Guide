"""Validate complete monthly batches, then write a versioned SQLite snapshot.
Usage: python F18_月度更新与版本冻结.py INPUT_FOLDER OUTPUT_FOLDER VERSION
Only Python's standard library is required. Existing versions are never replaced.
"""
from pathlib import Path
from decimal import Decimal
from datetime import date
import csv, hashlib, json, sqlite3, sys, re, tempfile, os

FIELDS=['SourceRow','Segment','Country','Product','Discount Band','Units Sold','Manufacturing Price','Sale Price','Gross Sales','Discounts','Sales','COGS','Profit','Date','Month Number','Month Name','Year']
NUMBERS=['Units Sold','Manufacturing Price','Sale Price','Gross Sales','Discounts','Sales','COGS','Profit']

def refresh(input_folder,output_folder,version):
    if not re.fullmatch(r'[A-Za-z0-9_-]+',version):
        raise ValueError('Version must use letters, numbers, underscores or hyphens.')
    source=Path(input_folder);out=Path(output_folder)
    files=sorted(source.glob('*.csv'))
    if not files:raise ValueError('No monthly CSV files found.')
    rows=[];ids=set();periods=[];hashes={}
    for f in files:
        if not re.fullmatch(r'\d{4}-\d{2}',f.stem):raise ValueError('Use exactly YYYY-MM.csv: '+f.name)
        period=f.stem;periods.append(period);hashes[f.name]=hashlib.sha256(f.read_bytes()).hexdigest()
        with f.open(encoding='utf-8-sig',newline='') as stream:
            reader=csv.DictReader(stream)
            if reader.fieldnames!=FIELDS:raise ValueError('Schema mismatch: '+f.name)
            batch=list(reader)
        if not batch:raise ValueError('Empty monthly batch: '+f.name)
        for row in batch:
            if any(row[k] is None or row[k].strip()=='' for k in FIELDS):raise ValueError('Missing required field: '+f.name)
            dt=date.fromisoformat(row['Date'])
            if dt.strftime('%Y-%m')!=period or dt.day!=1:raise ValueError('Period/date mismatch: '+f.name)
            if int(row['Year'])!=dt.year or int(row['Month Number'])!=dt.month:raise ValueError('Calendar mismatch: '+f.name)
            sid=int(row['SourceRow'])
            if sid in ids:raise ValueError('Repeated SourceRow in snapshot; investigate, do not deduplicate automatically.')
            ids.add(sid)
            n={k:Decimal(row[k]) for k in NUMBERS}
            if any(not v.is_finite() for v in n.values()):raise ValueError('Non-finite value: '+f.name)
            differences=[n['Units Sold']*n['Sale Price']-n['Gross Sales'],n['Gross Sales']-n['Discounts']-n['Sales'],n['Sales']-n['COGS']-n['Profit']]
            if any(abs(x)>Decimal('.01') for x in differences):raise ValueError('Amount reconciliation failed: '+f.name)
            rows.append([sid,period,row['Segment'],row['Country'],row['Product'],float(n['Units Sold']),float(n['Sales']),float(n['COGS']),float(n['Profit'])])
    monthnums=[int(p[:4])*12+int(p[5:]) for p in periods]
    if any(b-a!=1 for a,b in zip(monthnums,monthnums[1:])):raise ValueError('Missing month in the submitted sequence.')
    manifest={'version':version,'source_files':hashes,'months':periods,'rows':len(rows),'sales':float(sum(Decimal(str(r[6])) for r in rows)),'profit':float(sum(Decimal(str(r[8])) for r in rows)),'status':'validated sample snapshot','source_row_definition':'Technical trace ID, not a transaction ID.'}
    out.mkdir(parents=True,exist_ok=True);target=out/(version+'.sqlite')
    if target.exists():
        with sqlite3.connect(target) as db:old=json.loads(db.execute('SELECT json FROM manifest').fetchone()[0])
        if old==manifest:return {'status':'unchanged','manifest':manifest}
        raise ValueError('Frozen version differs. Use a new version; existing snapshot preserved.')
    fd,tmp=tempfile.mkstemp(dir=out,suffix='.sqlite');os.close(fd)
    try:
        with sqlite3.connect(tmp) as db:
            db.execute('CREATE TABLE actuals(source_row INTEGER PRIMARY KEY,month TEXT,segment TEXT,country TEXT,product TEXT,units REAL,sales REAL,cogs REAL,profit REAL)')
            db.executemany('INSERT INTO actuals VALUES(?,?,?,?,?,?,?,?,?)',rows)
            db.execute('CREATE VIEW monthly AS SELECT month,COUNT(*) records,SUM(sales) sales,SUM(cogs) cogs,SUM(profit) profit FROM actuals GROUP BY month')
            db.execute('CREATE TABLE manifest(json TEXT NOT NULL)');db.execute('INSERT INTO manifest VALUES(?)',(json.dumps(manifest,ensure_ascii=False),))
        os.link(tmp,target)  # Exclusive publication: fails if another writer created the version.
    finally:Path(tmp).unlink(missing_ok=True)
    return {'status':'created','manifest':manifest}

if __name__=='__main__':
    if len(sys.argv)!=4:raise SystemExit(__doc__)
    print(json.dumps(refresh(*sys.argv[1:]),ensure_ascii=False,indent=2))
