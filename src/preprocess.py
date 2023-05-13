import configparser
import os
import pandas as pd
from sklearn.model_selection import train_test_split
import traceback
import argparse

import pickle
import re
import string

from sklearn.feature_extraction.text import TfidfVectorizer
import sys
sys.path
import nltk
from nltk.tokenize import word_tokenize

from logger import Logger

SHOW_LOG = True

parser = argparse.ArgumentParser(description="Predictor")
parser.add_argument("--folder_path",
                    type=str,
                    help="Path to the folder",
                    default="data/raw_data/example")
parser.add_argument("--file_name",
                    type=str,
                    help="Name of the main file",
                    default="data_example.csv")
parser.add_argument("--split_scale",
                    type=float,
                    help="how to split data into train and test",
                    default=0.5)
parser.add_argument("--max_features",
                    type=float,
                    help="Parameter for TfidfVectorizer",
                    default=500000)
parser.add_argument("--ngrams",
                    type=float,
                    help="Parameter for TfidfVectorizer",
                    default=(1,2))
parser.add_argument("--train_vectoriser",
                    type=float,
                    help="Train own vectoriser or use pretrained",
                    default=True)
args = parser.parse_args()

# Defining set containing all stopwords in English :
stopwordlist = ['a', 'about', 'above', 'after', 'again', 'ain', 'all', 'am', 'an',
                'and', 'any', 'are', 'as', 'at', 'be', 'because', 'been', 'before',
                'being', 'below', 'between', 'both', 'by', 'can', 'd', 'did', 'do',
                'does', 'doing', 'down', 'during', 'each', 'few', 'for', 'from',
                'further', 'had', 'has', 'have', 'having', 'he', 'her', 'here',
                'hers', 'herself', 'him', 'himself', 'his', 'how', 'i', 'if', 'in',
                'into', 'is', 'it', 'its', 'itself', 'just', 'll', 'm', 'ma',
                'me', 'more', 'most', 'my', 'myself', 'now', 'o', 'of', 'on', 'once',
                'only', 'or', 'other', 'our', 'ours', 'ourselves', 'out', 'own', 're',
                's', 'same', 'she', "shes", 'should', "shouldve", 'so', 'some', 'such',
                't', 'than', 'that', "thatll", 'the', 'their', 'theirs', 'them',
                'themselves', 'then', 'there', 'these', 'they', 'this', 'those',
                'through', 'to', 'too', 'under', 'until', 'up', 've', 'very', 'was',
                'we', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom',
                'why', 'will', 'with', 'won', 'y', 'you', "youd", "youll", "youre",
                "youve", 'your', 'yours', 'yourself', 'yourselves']


def suffix_finder(sent):
    pattern = r'\.?\w+'
    find_sp = re.findall(pattern, sent)
    name, suffix = find_sp[0], find_sp[1]
    return name, suffix
# Cleaning and removing the above stop words list from the tweet text :
def cleaning_stopwords(text):
    STOPWORDS = set(stopwordlist)
    return " ".join([word for word in str(text).split() if word not in STOPWORDS])

#  Cleaning and removing punctuations :
def cleaning_punctuations(text):
    english_punctuations = string.punctuation
    punctuations_list = english_punctuations
    translator = str.maketrans('', '', punctuations_list)
    return text.translate(translator)

# Cleaning and removing URL’s :
def cleaning_URLs(data):
    return re.sub('((www.[^s]+)|(https?://[^s]+))', ' ', data)

# Cleaning and removing Numeric numbers :
def cleaning_numbers(data):
    return re.sub('[0-9]+', '', data)

# Applying Stemming :
def stemming_on_text(data):
    st = nltk.PorterStemmer()
    text = [st.stem(word) for word in data]
    return text

# Applying Lemmatizer :
def lemmatizer_on_text(data):
    lm = nltk.WordNetLemmatizer()
    text = [lm.lemmatize(word) for word in data]
    return text
class DataMaker():

    def __init__(self) -> None:
        logger = Logger(SHOW_LOG)
        self.config = configparser.ConfigParser()
        self.log = logger.get_logger(__name__)
        self.data_path = os.path.join(args.folder_path, args.file_name)
        self.X_path = os.path.join(args.folder_path, 'X_' + args.file_name)
        self.y_path = os.path.join(args.folder_path, 'y_' + args.file_name)
        self.name, self.suffix = suffix_finder(args.file_name)
        self.train_path = [os.path.join(args.folder_path, 'X_train_' + self.name +'.pickle'), os.path.join(args.folder_path, 'y_train_' + '.pickle')]
        self.test_path = [os.path.join(args.folder_path, 'X_test_' + self.name +'.pickle'), os.path.join(args.folder_path, 'y_test_' + '.pickle')]
        self.current_path = os.path.join(os.getcwd(), 'src')
        self.LOG_REG_path = os.path.join(self.current_path, 'experiments', 'LR.pickle')
        self.SVM_path = os.path.join(self.current_path, 'experiments', 'SVM.pickle')
        self.BNB_path = os.path.join(self.current_path, 'experiments', 'BNB.pickle')
        self.Vectoriser_path = os.path.join(self.current_path, 'experiments', 'Vectoriser.pickle')
        self.log.info("DataMaker is ready")
        try:
            self.config.read('config.ini')
        except UnicodeDecodeError as er:
            self.config.read('config.ini', encoding='latin-1')

    def get_data(self) -> bool:

        dataset = pd.read_csv(self.data_path)
        # Preprocessing text with function above the DataMaker class
        dataset['text'] = dataset['text'].str.lower() # Lower characters
        dataset['text'] = dataset['text'].apply(lambda text: cleaning_stopwords(text))
        dataset['text'] = dataset['text'].apply(lambda x: cleaning_punctuations(x))
        dataset['text'] = dataset['text'].apply(lambda x: cleaning_URLs(x))
        dataset['text'] = dataset['text'].apply(lambda x: cleaning_numbers(x))
        # Getting tokenization of tweet text
        nltk.download('punkt')
        dataset['text'] = dataset['text'].apply(word_tokenize)
        # Applying Stemming :
        dataset['text'] = dataset['text'].apply(lambda x: stemming_on_text(x))
        # Applying Lemmatization
        nltk.download('wordnet')
        nltk.download('omw-1.4')
        dataset['text'] = dataset['text'].apply(lambda x: lemmatizer_on_text(x))
        # Split to y and X
        X = pd.DataFrame(dataset['text'])
        y = pd.DataFrame(dataset['target'])
        X.to_csv(self.X_path, index=False)
        y.to_csv(self.y_path, index=False)
        if os.path.isfile(self.X_path) and os.path.isfile(self.y_path):
            self.log.info("X and y data is ready")
            self.config["DATA"] = {'X_data': self.X_path,
                                   'y_data': self.y_path}
            return os.path.isfile(self.X_path) and os.path.isfile(self.y_path)
        else:
            self.log.error("X and y data is not ready")
            return False

    def split_data(self, test_size=args.split_scale) -> bool:
        self.get_data()
        try:
            X = pd.read_csv(self.X_path)['text']
            y = pd.read_csv(self.y_path)['target']
        except FileNotFoundError:
            self.log.error(traceback.format_exc())
            sys.exit(1)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=0)
        # Applying vectorization
        if args.train_vectoriser:
            vectoriser = TfidfVectorizer(ngram_range=args.ngrams, max_features=args.max_features)
            vectoriser.fit(X_train)
            with open(self.Vectoriser_path, 'wb') as f:
                pickle.dump(vectoriser, f)
        else:
            vectoriser = pickle.load(open(self.Vectoriser_path, "rb"))
        X_train = vectoriser.transform(X_train)
        X_test = vectoriser.transform(X_test)
        # Save data to the final pickle format
        self.save_splitted_data(X_train, self.train_path[0])
        self.save_splitted_data(y_train, self.train_path[1])
        self.save_splitted_data(X_test, self.test_path[0])
        self.save_splitted_data(y_test, self.test_path[1])
        self.config["SPLIT_DATA"] = {'X_train': self.train_path[0],
                                     'y_train': self.train_path[1],
                                     'X_test': self.test_path[0],
                                     'y_test': self.test_path[1]}

        self.config["BNB"] = {'path': self.BNB_path}
        self.config["SVM"] = {'path': self.SVM_path}
        self.config["LOG_REG"] = {'path': self.LOG_REG_path}
        self.config["Vectoriser"] = {'path': self.Vectoriser_path}
        self.log.info("Train and test data is ready")
        with open(os.path.join(self.current_path, "config.ini"), 'w') as configfile:
            self.config.write(configfile)
        return os.path.isfile(self.train_path[0]) and\
            os.path.isfile(self.train_path[1]) and\
            os.path.isfile(self.test_path[0]) and \
            os.path.isfile(self.test_path[1])

    def save_splitted_data(self, df, path: str) -> bool:
        pickle.dump(df, open(path, 'wb'))
        self.log.info(f'{path} is saved')
        return os.path.isfile(path)


if __name__ == "__main__":
    data_maker = DataMaker()
    data_maker.split_data()
