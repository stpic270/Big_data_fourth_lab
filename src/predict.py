import argparse
import configparser
import os
import shutil
import time
from datetime import datetime
import re
import pickle
import sys
import yaml

import traceback
from utils import model_Evaluate, graphic

from logger import Logger

SHOW_LOG = True


class Predictor():

    def __init__(self) -> None:
        """
        Initialization the paths and parser
        """
        logger = Logger(SHOW_LOG)
        self.config = configparser.ConfigParser()
        self.log = logger.get_logger(__name__)
        self.current_path = os.path.join(os.getcwd())
        self.config.read(os.path.join(self.current_path, "src", "config.ini"))
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
        self.parser.add_argument("-t",
                                 "--tests",
                                 type=str,
                                 help="Select tests",
                                 required=True,
                                 default="smoke",
                                 const="smoke",
                                 nargs="?",
                                 choices=["smoke", "func"])
        self.X_train = pickle.load(open(os.path.join(self.current_path, self.config["SPLIT_DATA"]["X_train"]), 'rb'))
        self.y_train = pickle.load(open(os.path.join(self.current_path, self.config["SPLIT_DATA"]["y_train"]), 'rb'))
        self.X_test = pickle.load(open(os.path.join(self.current_path, self.config["SPLIT_DATA"]["X_test"]), 'rb'))
        self.y_test = pickle.load(open(os.path.join(self.current_path, self.config["SPLIT_DATA"]["y_test"]), 'rb'))
        self.log.info("Predictor is ready")


    def predict(self) -> bool:
        "Prediction on the tests with chosen model"
        args = self.parser.parse_args()
        try:
            classifier = pickle.load(
                open(os.path.join(self.current_path, self.config[args.model]["path"]), "rb"))
        except FileNotFoundError:
            self.log.error(traceback.format_exc())
            sys.exit(1)

        if args.tests == "smoke":
            try:
                score = classifier.predict(self.X_test)
                model_Evaluate(score, self.y_test)
                graphic(self.y_test, score)
                print(f'{args.model} has {score} score')
            except Exception:
                self.log.error(traceback.format_exc())
                sys.exit(1)
            self.log.info(f'{self.config[args.model]["path"]} passed smoke tests')

        elif args.tests == "func":

            exp_path = os.path.join(self.current_path, "src", "experiments")

            try:
                score = classifier.predict(self.X_test)
                print(f'{args.model} has {score} score')
            except Exception:
                self.log.error(traceback.format_exc())
                sys.exit(1)

            # Find name of file without extension
            s = self.config["SPLIT_DATA"]["x_train"]
            pattern = r'\w+.pickle'
            name = re.findall(pattern, s)[0].replace('X_', '').replace('.pickle', '')
            # Create logs
            self.log.info(
                f'{self.config[args.model]["path"]} passed func test {name}')
            exp_data = {
                "model": args.model,
                "model params": dict(self.config.items(args.model)),
                "tests": args.tests,
                "score": str(score),
                "X_test path": self.config["SPLIT_DATA"]["x_test"],
                "y_test path": self.config["SPLIT_DATA"]["y_test"],
            }
            date_time = datetime.fromtimestamp(time.time())
            str_date_time = date_time.strftime("%Y_%m_%d_%H_%M_%S")
            exp_dir = os.path.join(exp_path, f'exp_{name}_{str_date_time}')
            os.mkdir(exp_dir)
            # Dump logs
            with open(os.path.join(exp_dir, "exp_config.yaml"), 'w') as exp_f:
                yaml.safe_dump(exp_data, exp_f, sort_keys=False)
            # Output results
            model_Evaluate(score, self.y_test, os.path.join(exp_dir, "conf_matrix.png"))
            graphic(self.y_test, score, os.path.join(exp_dir, "praph.png"))
            shutil.copy(os.path.join(os.getcwd(), "src", "logfile.log"), os.path.join(exp_dir, "exp_logfile.log"))
            shutil.copy(self.config[args.model]["path"], os.path.join(exp_dir, f'exp_{args.model}.sav'))
        return True


if __name__ == "__main__":
    predictor = Predictor()
    predictor.predict()
