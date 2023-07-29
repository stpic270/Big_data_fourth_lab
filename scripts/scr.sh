#!/bin/bash
ansible-vault encrypt --vault-password-file my_password.txt test/cassandra_config.txt 
echo "Sleeping had started"
sleep infinity
echo "Sleeping has ended"
