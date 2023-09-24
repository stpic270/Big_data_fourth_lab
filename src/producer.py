from kafka import KafkaProducer 
from utils import get_session, send_message_from_cassandra
import cassandra

# Create producer
producer = KafkaProducer(bootstrap_servers=['kafka:9092'])

# Get session
session = get_session()

# Create namespaces and tables
for m in ['BNB', 'SVM', 'LOG_REG']:
  send_message_from_cassandra(m, session, producer)

# Delete credentials
with open("test/cassandra_config.txt", "r") as f:
  lines = f.readlines()
with open("test/cassandra_config.txt", "w") as f:
  for line in lines:
    
    f.write('data uploaded to cassandra successful, secrets are removed\n')