<<<<<<< HEAD
# Big_data_second_lab
=======
# Semantic analysis 
Анализ настроений относится к выявлению, а также к классификации настроений, выраженных в источнике текста. Твиты часто полезны для создания огромного количества данных о настроениях после анализа. Эти данные полезны для понимания мнения людей по различным темам.

В данной работе был обучен семантические классификаторы для определения является ли предложение позитивным или негативным. В качестве моделей использовались классификаторы библиотеки sklearn: SVC, LogisticRegression, BernoulliNB. В качестве тестовых и тренировочных данных использовался корпус https://www.kaggle.com/datasets/kazanova/sentiment140, который был предобработан и передан  библиотеке nltk для операций стемминга, токенизации и лемматизации. Также использовался TfidfVectorizer библиотеки sklearn для векторизации данных.

## Notebook
Более подробно с предобработкой корпуса и тренировкой моделей можно ознакомиться в ноутбуке notebooks/First_lab_BD.ipynb.  

## DVC и исходники
В связи с тем, что тренировочные файлы и веса TfidfVectorizer весят слишком много, к ним был применен dvc с кэшированием на локальном компьютере. Исходники для скачивания доступны по ссылке - https://drive.google.com/drive/folders/1zn2KNDN-BjL2o4Q2og8KVEdXJzWYF6Jv?usp=sharing
X_train_vectoriser.pickle - 95% от основного корпуса предобработанных тренировочных данных
y_train_vectoriser.pickle - метки для тренировочного набора 
Vectoriser.pickle - веса для TfidfVectorizer, обученного на предобработанном X_train для векторизации.



## Тесты 
inference.py - выводит результаты модели на X_test_vectoriser.pickle, необходимо указать модель. Пример:
python inference.py -m LOG_REG
src/preprocess.py - скрипт, который преобразовывает данные формата csv для последующей тренировки и теста.  
При использовании своих корпусов необходимо положить файл формат csv в папку data/raw_data/name_your_directory/name_your_csv. И указать путь к папке и название файла csv, пример:
python src/preprocess.py --folder_path name_your_directory --file_name name_your_csv 

Эти данные равняются "data/raw_data/example" и "data_example.csv" по умолчанию. 
Также есть возможность использовать тренированный  TfidfVectorizer, с https://drive.google.com/drive/folders/1zn2KNDN-BjL2o4Q2og8KVEdXJzWYF6Jv?usp=sharing. Для его использования необходимо данный файл скачать в папку src/experiments/Vectoriser.pickle, и указать параметр --train_vectoriser False, пример:

python src/preprocess.py --folder_path name_your_directory --file_name name_your_csv --train_vectoriser False # (default = True).

Его веса останутся в src/experiments/Vectoriser.pickle. Также при тренировке собственного  TfidfVectorizer веса сохранятся в указанной папке. 
Используйте python src/preprocess.py —help для более детальной информации
src/train.py - скрипт для тренировке модели, необходимо указать модель, пример: 

python src/train.py -m SVM.

Веса тренированной модели будут лежать в папке src/experiments
src/predict.py - скрипт для проверке на данных после src/preprocess.py. Необходимо также указать модель, на которой производилась тренировка. Пример:

python src/predict.py -m SVM

По умолчанию в папке src/experiments уже лежат веса, полученные после тренировке на основном корпусе, после src/train.py вес для данной модели будет перезаписан. Эти веса также доступны для скачивания с https://drive.google.com/drive/folders/19Z2hMvKclQUKfNme4AY1jH09WIDnFzTj?usp=sharing
    
Результаты python inference.py -m SVM

![image](https://github.com/stpic270/Big_data_first_lab/assets/58371161/c9d40821-987c-45a2-a9af-2ef623e7e7b3)

Рис. 1 результаты python inference.py -m SVM

>>>>>>> bf60a8d8a249cf82531bda6daf7b2ef3d6261178
