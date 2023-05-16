import configparser
import os
import unittest
import pandas as pd
import sys

sys.path.insert(1, os.path.join(os.getcwd(), "src"))

from train import MultiModel

config = configparser.ConfigParser()
config.read("src/config.ini")


class TestMultiModel(unittest.TestCase):

    def setUp(self) -> None:
        self.multi_model = MultiModel()

    def test_log_reg(self):
        self.assertEqual(self.multi_model.log_reg(), True)

    def test_svm(self):
        self.assertEqual(self.multi_model.svm(use_config=False), True)

    def test_gnb(self):
        self.assertEqual(self.multi_model.bnb(), True)

if __name__ == "__main__":
    unittest.main()


