#!/bin/bash
ansible-vault decrypt --vault-password-file my_password.txt test/cassandra_config.txt
python use_cassandra.py
ansible-vault encrypt --vault-password-file my_password.txt test/cassandra_config.txt 