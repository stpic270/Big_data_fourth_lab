import cassandra
from utils import create_table, get_session

# Create Session
session = get_session()

# Create namespaces and tables
for m in ['BNB', 'SVM', 'LOG_REG']:
  create_table(m, session)

