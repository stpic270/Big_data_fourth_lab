# Semantic analysis outputs to cassandra using ansible and kafka

#### Описание работы модели семантического анализа находится по ссылке -https://github.com/stpic270/Big_data_first_lab.

В данном репозитории осуществляется выгрузка результатов работы модели семантического анализа в базу данных cassandra. При этом
используется ansible-vault, который зашифровывает пароль и логин при запуске контейнера. Кроме того, после передачи данных в cassandra, сообщения отсылаются с помощью библиотеки kafka python. Сообщения принимаются с помощью kafka consumer на отдельном для этого контейнере.
С помощью следующих шагов можно проделать данные операции:
1. Собрать и запустить контейнеры с помощью docker compose:
### - docker compose up -d --no-start
2. Запустить контейнеры базы данных и модели(подождать 30 секунд после запуска):
### - docker start big_data_third_lab-model-1 && docker start big_data_third_lab-cassandra-1
3. Выполнить следующие команды для передачи ip адресса базы данных.
### - docker exec -t big_data_third_lab-cassandra-1 bash -c "echo '\n' >> config/cassandra_ip.txt && ip -4 -o address >> config/cassandra_ip.txt"
4. Запустить контейнеры kafka и zookeeper (подождать 2 мин после запуска):
### - docker start big_data_fourth_lab-zookeeper-1
### - docker start big_data_fourth_lab-kafka-1 && docker exec -t -d big_data_fourth_lab-kafka-1 bash -c "/bin/kafka-topics --create --topic cassandra-topic --bootstrap-server kafka:9092"
5. Выполнить следующие команды для передачи данных в cassandra и отправки сообщений с помощью producer, а также для считывания 12-ти отправленных данных с помощью consumer. Кроме того, после отправки данных, как и в прошлой работе последует УДАЛЕНИЕ логина и пароля из файла:
### - docker exec -t big_data_fourth_lab-model-1 bash -c "scripts/cassandra.sh"
### - docker exec -t big_data_fourth_lab-kafka-1 bash -c "/bin/kafka-console-consumer --topic cassandra-topic --max-messages 12 --from-beginning --bootstrap-server kafka:9092"
Однако при запуске контейнера с базой данной необходимо ждать некоторое количество времени, при этом программа будет информировать об этом и засыпать каждые 40 с. Кроме того, иногда не удается подключиться к стабильно работающему контейнеру, используемый скрипт use_cassandra.py также будет информировать об этом и брать паузы в 10 с. В результате корректной работы программы, результаты модели будут взяты из контейнера cassandra и выведены в log, как на картинке

![image](https://github.com/stpic270/Big_data_fourth_lab/assets/58371161/91fc85d9-401f-4543-bc5a-189412886fbb)

Рис. 1 - корректная передача метрик в базу данных

В результате корректной работы producer и consumer, из контейнера kafka будут выведены 12 строк, такого же формата, что и на рис. 1