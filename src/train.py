import configparser
import os
import pickle
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import accuracy_score

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
import sys
import traceback

from logger import Logger

SHOW_LOG = True
import argparse

parser = argparse.ArgumentParser(description="Predictor")
parser.add_argument( "-m",
                     "--model",
                     type=str,
                     help="Select model",
                     required=True,
                     default="LOG_REG",
                     const="LOG_REG",
                     nargs="?",
                     choices=["LOG_REG", "BNB", "SVM"])

class MultiModel():

    def __init__(self) -> None:
        logger = Logger(SHOW_LOG)
        self.config = configparser.ConfigParser()
        self.log = logger.get_logger(__name__)
        self.current_path = os.getcwd()
        self.config.read(os.path.join(self.current_path, "config.ini"))

        self.X_train = pickle.load(open(os.path.join(self.current_path, self.config["SPLIT_DATA"]["X_train"]), 'rb'))
        self.y_train = pickle.load(open(os.path.join(self.current_path, self.config["SPLIT_DATA"]["y_train"]), 'rb'))
        self.X_test = pickle.load(open(os.path.join(self.current_path, self.config["SPLIT_DATA"]["X_test"]), 'rb'))
        self.y_test = pickle.load(open(os.path.join(self.current_path, self.config["SPLIT_DATA"]["y_test"]), 'rb'))

        self.project_path = os.path.join(self.current_path, "experiments")
        self.log_reg_path = os.path.join(self.project_path, "LR.pickle")
        self.svm_path = os.path.join(self.project_path, "SVM.pickle")
        self.gnb_path = os.path.join(self.project_path, "BNB.pickle")
        self.log.info("MultiModel is ready")

    def log_reg(self, predict=False, max_iter = 200) -> bool:
        classifier = LogisticRegression(max_iter=max_iter)
        try:
            classifier.fit(self.X_train, self.y_train)
        except Exception:
            self.log.error(traceback.format_exc())
            sys.exit(1)
        if predict:
            y_pred = classifier.predict(self.X_test)
            print(accuracy_score(self.y_test, y_pred))
        params = {'path': self.log_reg_path}
        return self.save_model(classifier, self.log_reg_path, "LOG_REG", params)

    def svm(self, use_config: bool, kernel="linear", random_state=0, predict=False) -> bool:
        if use_config:
            try:
                classifier = SVC(kernel=self.config["SVM"]["kernel"], random_state=self.config.getint(
                    "SVC", "random_state"))
            except KeyError:
                self.log.error(traceback.format_exc())
                self.log.warning(f'Using config:{use_config}, no params')
                sys.exit(1)
        else:
            classifier = SVC(kernel=kernel, random_state=random_state)
        try:
            classifier.fit(self.X_train, self.y_train)
        except Exception:
            self.log.error(traceback.format_exc())
            sys.exit(1)
        if predict:
            y_pred = classifier.predict(self.X_test)
            print(accuracy_score(self.y_test, y_pred))
        params = {'kernel': kernel,
                  'random_state': random_state,
                  'path': self.svm_path}
        return self.save_model(classifier, self.svm_path, "SVM", params)

    def bnb(self, predict=False) -> bool:
        classifier = BernoulliNB()
        try:
            classifier.fit(self.X_train, self.y_train)
        except Exception:
            self.log.error(traceback.format_exc())
            sys.exit(1)
        if predict:
            y_pred = classifier.predict(self.X_test)
            print(accuracy_score(self.y_test, y_pred))
        params = {'path': self.gnb_path}
        return self.save_model(classifier, self.gnb_path, "GNB", params)

    def save_model(self, classifier, path: str, name: str, params: dict) -> bool:
        self.config[name] = params
        os.remove(os.path.join(self.current_path, "config.ini"))
        with open(os.path.join(self.current_path, "config.ini"), 'w') as configfile:
            self.config.write(configfile)
        with open(path, 'wb') as f:
            pickle.dump(classifier, f)

        self.log.info(f'{path} is saved')
        return os.path.isfile(path)


if __name__ == "__main__":
    args = parser.parse_args()
    multi_model = MultiModel()
    if args.model == 'LOG_REG':
        multi_model.log_reg(predict=True, max_iter=200)
    if args.model == 'SVM':
        multi_model.svm(use_config=False, predict=True)
    if args.model == 'BNB':
        multi_model.bnb(predict=True)

#model_Evaluate(BNBmodel)


