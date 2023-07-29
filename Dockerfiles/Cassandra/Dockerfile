FROM cassandra:latest

RUN echo authenticator: PasswordAuthenticator >> /etc/cassandra/cassandra.yaml &&\
    echo read_request_timeout: 60000ms >> /etc/cassandra/cassandra.yaml &&\
    echo range_request_timeout: 60000ms >> /etc/cassandra/cassandra.yaml &&\
    echo write_request_timeout: 60000ms >> /etc/cassandra/cassandra.yaml &&\
    echo counter_write_request_timeout: 60000ms >> /etc/cassandra/cassandra.yaml &&\
    echo cas_contention_timeout: 60000ms >> /etc/cassandra/cassandra.yaml &&\
    echo request_timeout: 60000ms >> /etc/cassandra/cassandra.yaml &&\

# RUN bash -c "ip -4 -o address >> config/cassandra_config.txt"