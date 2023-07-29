FROM python:3.8-slim

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

WORKDIR /app

COPY . /app

RUN chmod +x scripts/scr.sh && chmod +x scripts/cassandra.sh && pip install -r requirements.txt && \
    python inference.py -m SVM &&  apt-get update && apt-get install pwgen -y &&\
    echo $(pwgen 14 1) >> my_password.txt && apt-get install nano &&\
    apt install krb5-user -y && apt-get install ansible -y
    
ENTRYPOINT ["scripts/scr.sh"]