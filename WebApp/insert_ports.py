import pandas as pd
from utils import get_database
import pymongo
import json

df = pd.read_csv('wpi_merge_wld_trs_ports_wfp_limited_fields.csv',delimiter='\t',header=None,names=['PortName','lat','lon','Size','Type','Country','source'])
df['location'] = 0
for i,r in df.iterrows():
    df.loc[i,'location'] = '{"type":"Point","coordinates":[%f,%f]}'%(r['lon'],r['lat'])
print(df.location)
j = df.to_json(orient='records')

j = json.loads(j)
for d in j:
    d['location'] = json.loads(d['location'])
print(j)
db = get_database()
db.ports.insert_many(j)
db.ports.create_index([('location':pymongo.GEOSPHERE)])