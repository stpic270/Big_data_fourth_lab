# Semantic analysis outputs to cassandra using ansible

Описание работы модели семантического анализа находится по ссылке - https://github.com/stpic270/Big_data_first_lab. 

В данном репозитории осуществляется выгрузка результатов работы моделкй семантического анализа в базу данных cassandra. При этом используется ansible-vault, который зашифровывает пароль и логин при запуске контейнера. С помощью следующих шагов можно проделать данные операции:
1) Собрать и запустить контейнеры с помощью docker compose:
   ### docker compose build && docker compose up -d --no-start
2) Запустить контейнеры базы данных и модели:
   ### docker start big_data_third_lab-model-1 && docker start big_data_third_lab-cassandra-1
3) Выполнить следующие команды для передачи ip адресса базы данных и запуска скрипта с шифрованием и УДАЛЕНИЕМ логина и паролей из файла:
   ### docker exec -t big_data_third_lab-cassandra-1 bash -c "echo '\n' >> config/cassandra_ip.txt && ip -4 -o address >> config/cassandra_ip.txt"
   ### docker exec -t big_data_third_lab-model-1 bash -c "scripts/cassandra.sh"
Однако при запуске контейнера с базой данной необходимо ждать некоторое количество времени, при этом программа будет информировать об 
этом и засыпать каждые 40 с. Кроме того, иногда не удается подключиться к стабильно работающему контейнеру, используемый скрипт use_cassandra.py также будет информировать об этом и брать паузы в 10 с. В результате корректной работы программы, результаты модели будут взяты из контейнера cassandra и выведены в log, как на картинке 

![image](https://github.com/stpic270/Big_data_second_lab/assets/58371161/93e7f011-eb30-4524-804e-e0814a26d4fc)

Рис. 1 - корректная передача метрик в базу данных
