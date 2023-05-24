from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster
import os
import re

credentials = []
pattern =r'(\d+.\d+.\d+.\d+)/\d+'

l, p = 'login:', 'password:'
with open('test/cassandra_config.txt', 'r') as f:
  for line in f:
    s = line.strip()
    if l in s:
      le = len(l)
      credentials.append(line.strip()[le:])
    if p in s:
      le = len(p)
      credentials.append(line.strip()[le:])
    if '172.' in s:
      sp = re.findall(pattern, s)
      credentials.append(sp[0])
  f.close
print(credentials)
auth_provider = PlainTextAuthProvider(username=credentials[0], password=credentials[1])

# Connect to the cluster's default port
cluster = Cluster([credentials[2]], port=9042, auth_provider=auth_provider)
session = cluster.connect()

def create_table(folder):
  folder = folder.lower()
  s = "CREATE KEYSPACE IF NOT EXISTS WITH REPLICATION={'class':'SimpleStrategy', 'replication_factor':5};"
  s = s.split()
  s.insert(5, f'{folder}')
  s = ' '.join(s)

  session.execute(s)
  # Connect to music_store
  session.execute(f"USE {folder};")
  path = f'test/{folder}'
  if not os.path.exists(path):
    print(f'There is not folder {folder} hence there are not csv files of {folder} model to import to cassandra')
    return None
  for file in os.listdir(path):

    path_f = f'test/{folder}/{file}'
    file = file.replace('.csv', '')

    q = f"CREATE TABLE IF NOT EXISTS {file} (labels_name text, precision float, recall float, f1_score float, PRIMARY KEY(labels_name));"
    session.execute(q)

    prepared = session.prepare(f"INSERT INTO {file} (labels_name, precision, recall, f1_score) VALUES (?, ?, ?, ?)")
    with open(path_f, "r") as fares:
      for fare in fares:
        columns=fare.split(",")
        if 'labels_name' in columns:
          continue
        ln=columns[0]
        pr=float(columns[1])
        re=float(columns[2])
        f1=float(columns[3])

        session.execute(prepared, [ln,pr,re,f1])

    #closing the file
    fares.close()
  rows = session.execute(f"SELECT * FROM {file}")
  for i in rows:
    print(i)

for m in ['BNB', 'SVM', 'LOG_REG']:
  create_table(m)
