#!/bin/bash
ansible-vault decrypt --vault-password-file my_password.txt test/cassandra_config.txt
python src/use_cassandra.py
python src/producer.py
ansible-vault encrypt --vault-password-file my_password.txt test/cassandra_config.txt 
python src/consumer.py