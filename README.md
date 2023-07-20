# Semantic analysis outputs to cassandra

Описание работы модели семантического анализа находится по ссылке - https://github.com/stpic270/Big_data_first_lab. 

В данном репозитории добавлен файл use_cassandra.py, который позволяет модели взаимодействовать с базой данных cassandra с использованием docker container

Для этого необходимо использовать docker images: stpic270/bd-secl-cassandra:latest, stpic270/bd-secl-d:latest и выполнить следующие команды:

1) Запуск container. После запуска необходимо подождать некоторое время (5-7 минут) для корректной работы базы данных - docker run --name cassandra -v big_data_second_lab_cassandra_config:/config -e HEAP_NEWSIZE=1M -e MAX_HEAP_SIZE=1024M -t -d -p 9042:9042 stpic270/bd-secl-cassandra

2) Передать ip адреса в volume - docker exec -t cassandra bash -c "echo '\n' >> config/cassandra_config.txt && ip -4 -o address >> config/cassandra_config.txt"

3) Использовать use_cassandra.py для выгрузки метрик в базу данных - docker run --name model -v big_data_second_lab_cassandra_config:/app/test -t -i -p 71:70 stpic270/bd-secl-d bash -c 'python use_cassandra.py'

4) Иногда может возникнуть ошибка, связанная с долгим ожиданием ответа от базы данных - Client request timeout:

![image](https://github.com/stpic270/Big_data_second_lab/assets/58371161/9ba4d039-d113-4fee-aa11-085ca1169c5f)

Рис. 1 - ошибка из-за долгого ожидания ответа

Тогда необходимо просто запустить container с моделью еще раз - docker start model. Корректный вывод должен содержать пример метрик, переданных в базу данных cassandra:

![image](https://github.com/stpic270/Big_data_second_lab/assets/58371161/93e7f011-eb30-4524-804e-e0814a26d4fc)

Рис. 2 - корректная передача метрик в базу данных

5) Также после корректного вывода, либо при удалении и новом запуске model, config с ip адрессом базы данных стирается и необходимо выполнить снова пункт 2.
