FROM python:3.8-slim

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt && python inference.py -m SVM &&  apt-get update && apt-get install pwgen -y &&\
    echo $(pwgen 14 1) >> my_password.txt && \
    apt install krb5-user -y && apt-get install ansible -y
    
CMD ["ansible-vault", "encrypt", "--vault-password-file", "my_password.txt", "test/cassandra_config.txt"]