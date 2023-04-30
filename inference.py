import argparse
import configparser
import os

import pickle
import sys

import traceback
from src.utils import model_Evaluate, graphic

from src.logger import Logger

SHOW_LOG = True


class Predictor():

    def __init__(self) -> None:
        logger = Logger(SHOW_LOG)
        self.config = configparser.ConfigParser()
        self.log = logger.get_logger(__name__)
        self.current_path = os.getcwd()

        self.config.read(os.path.join(self.current_path, "main_config.ini"))
        self.parser = argparse.ArgumentParser(description="Predictor")
        self.parser.add_argument("-m",
                                 "--model",
                                 type=str,
                                 help="Select model",
                                 required=True,
                                 default="LOG_REG",
                                 const="LOG_REG",
                                 nargs="?",
                                 choices=["LOG_REG", "BNB", "SVM"])

        self.X_train = pickle.load(open(os.path.join(self.current_path, self.config["SPLIT_DATA"]["X_train"]), 'rb'))
        self.y_train = pickle.load(open(os.path.join(self.current_path, self.config["SPLIT_DATA"]["y_train"]), 'rb'))
        self.X_test = pickle.load(open(os.path.join(self.current_path, self.config["SPLIT_DATA"]["X_test"]), 'rb'))
        self.y_test = pickle.load(open(os.path.join(self.current_path, self.config["SPLIT_DATA"]["y_test"]), 'rb'))
        self.log.info("Predictor is ready")


    def predict(self) -> bool:
        args = self.parser.parse_args()
        try:
            classifier = pickle.load(
                open(os.path.join(self.current_path, self.config[args.model]["path"]), "rb"))
        except FileNotFoundError:
            self.log.error(traceback.format_exc())
            sys.exit(1)

        try:
            score = classifier.predict(self.X_test)
            model_Evaluate(score, self.y_test)
            graphic(self.y_test, score)
            print(f'{args.model} has {score} score')
        except Exception:
            self.log.error(traceback.format_exc())
            sys.exit(1)
        self.log.info(
            f'{self.config[args.model]["path"]} passed tests')

        return True


if __name__ == "__main__":
    predictor = Predictor()
    predictor.predict()