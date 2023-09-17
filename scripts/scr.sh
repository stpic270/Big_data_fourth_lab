#!/bin/bash
ansible-vault encrypt --vault-password-file my_password.txt test/cassandra_config.txt 
python src/preprocess.py && python src/train.py -m BNB && python src/predict.py -m BNB -t func && coverage run src/unit_tests/test_preprocess.py && coverage run -a src/unit_tests/test_training.py && coverage report -m
sleep infinity

