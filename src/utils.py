import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.metrics import roc_curve, auc
import pandas as pd
import os
import cassandra
import time
from kafka import KafkaProducer
import re
import json

def model_Evaluate(y_pred, y_test, model, suffix=None, savepath_graph=None, save_csv=False):
    """
    Plot confusion matrix
    """
    model = model.lower()
    # Print the evaluation metrics for the dataset and make CSV file.
    target_names = ['negative label', 'positive label']
    report = classification_report(y_test, y_pred, output_dict=True, target_names=target_names)
    df = pd.DataFrame.from_dict(report).T
    df = df.drop(['support'], axis=1)
    df = df.rename(columns={'f1-score':'f1_score'})
    df.index.name = 'labels_name'
    print(df)
    if save_csv==True and suffix != None:
        if not os.path.exists(f'test/{model}'):
            os.mkdir(f'test/{model}')
        number_of_tests = len([f for f in os.listdir(f'test/{model}') if suffix in f])
        savepath_csv = f'test/{model}/{suffix}_{number_of_tests}.csv'
        df.to_csv(savepath_csv)
    # Compute and plot the Confusion matrix
    cf_matrix = confusion_matrix(y_test, y_pred)
    categories = ['Negative','Positive']
    group_names = ['True Neg','False Pos', 'False Neg','True Pos']
    group_percentages = ['{0:.2%}'.format(value) for value in cf_matrix.flatten() / np.sum(cf_matrix)]
    labels = [f'{v1}n{v2}' for v1, v2 in zip(group_names,group_percentages)]
    labels = np.asarray(labels).reshape(2,2)
    sns.heatmap(cf_matrix, annot = labels, cmap = 'Blues',fmt = '',
    xticklabels = categories, yticklabels = categories)
    plt.xlabel("Predicted values", fontdict = {'size':14}, labelpad = 10)
    plt.ylabel("Actual values" , fontdict = {'size':14}, labelpad = 10)
    plt.title ("Confusion Matrix", fontdict = {'size':18}, pad = 20)
    if savepath_graph is None:
        plt.show()
    else:
        plt.savefig(savepath_graph)

def graphic(y_test, y_pred, savepath=None):
    """
    Plot ROC AUC graph
    """
    fpr, tpr, thresholds = roc_curve(y_test, y_pred)
    roc_auc = auc(fpr, tpr)
    plt.figure()
    plt.plot(fpr, tpr, color='darkorange', lw=1, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC CURVE')
    plt.legend(loc="lower right")
    if savepath is None:
        plt.show()
    else:
        plt.savefig(savepath)

# Execute query 
def executions(ses, q):
  flag=True
  while flag==True:
    try:
      ses.execute(q)
      flag = False
    except cassandra.OperationTimedOut as er:
      print(er)
      print(f'This time cassandra did not answerimplement the {q} querry, program will sleep for 10s and try again')
      time.sleep(10)

def get_credentials():
    credentials = []
    l, p = 'login:', 'password:'
    with open('test/cassandra_config.txt', 'r') as f:
        for line in f:
            s = line.strip()
            if l in s:
                le = len(l)
                credentials.append(line.strip()[le:])
            if p in s:
                le = len(p)
                le2 = len(credentials[0])
                credentials.append(line.strip()[le:le+le2])
    f.close
    return credentials

def get_ip(credentials, pattern):
    with open('test/cassandra_ip.txt', 'r') as ip:
        for i, line in enumerate(ip):
            if '172.' in line or "eth0" in line:
                sp = re.findall(pattern, line)
                credentials.append(sp[0])
        ip.close 

    return credentials

def create_table(folder, session, producer):
  # Make query to create namespace
  folder = folder.lower()
  s = "CREATE KEYSPACE IF NOT EXISTS WITH REPLICATION={'class':'SimpleStrategy', 'replication_factor':5};"
  s = s.split()
  s.insert(5, f'{folder}')
  s = ' '.join(s)

  executions(session, s)
  # Connect to namespace
  executions(session, f"USE {folder};")
  path = f'test/{folder}'
  if not os.path.exists(path):
    print(f'There is not folder {folder} hence there are not csv files of {folder} model to import to cassandra')
    return None

  # List over csv files, create tables and transport data to cassandra
  for file in os.listdir(path):

    path_f = f'test/{folder}/{file}'
    file = file.replace('.csv', '')

    q = f"CREATE TABLE IF NOT EXISTS {file} (labels_name text, precision float, recall float, f1_score float, PRIMARY KEY(labels_name));"
    
    executions(session, q)

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

  # Read table data from svm namespace
  if folder == 'svm':
    print('Example of The following lines in cassandra database of svm model')
    rows = session.execute(f"SELECT * FROM {file}")
    for i in rows:
      print(i)

  # Send messages using producer
  rows = session.execute(f"SELECT * FROM {file}")
  producer.send('cassandra-topic', json.dumps(f'From folder {folder}: ').encode('utf-8'))
  for i in rows:
    producer.send('cassandra-topic', json.dumps(i).encode('utf-8'))