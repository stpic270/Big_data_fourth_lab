from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster
import os
import re
import cassandra
import time
import json
from kafka import KafkaProducer
from utils import create_table, get_credentials, get_ip, executions

# Pattern to get ip
pattern =r'(\d+.\d+.\d+.\d+)/\d+'

# Get credentials
credentials = get_credentials()
credentials = get_ip(credentials, pattern) # Add ip to credentials

auth_provider = PlainTextAuthProvider(username=credentials[0], password=credentials[1])

# Connect to cassandra
flag=True
while flag==True:
  try:
    cluster = Cluster([credentials[2]], port=9042, auth_provider=auth_provider)
    session = cluster.connect()
    flag = False
  except cassandra.cluster.NoHostAvailable as er:
    print(er)
    print('This time cassandra did not answer, program will sleep for 40s and  try again')
    time.sleep(40)

# Initialise produces to send message
producer = KafkaProducer(bootstrap_servers=['kafka:9092'])

# Create namespaces and tables
for m in ['BNB', 'SVM', 'LOG_REG']:
  create_table(m, session, producer)

# Delete credentials
with open("test/cassandra_config.txt", "r") as f:
  lines = f.readlines()
with open("test/cassandra_config.txt", "w") as f:
  for line in lines:
    
    f.write('data uploaded to cassandra successful, secrets are removed\n')
