from kafka import KafkaConsumer
import json

# Create consumer
consumer = KafkaConsumer('cassandra-topic', bootstrap_servers='kafka:9092', auto_offset_reset='earliest')

# Read first 12 messages
for i in range(12):
 
  m = json.loads(next(consumer).value.decode('utf-8'))
  print(m)
