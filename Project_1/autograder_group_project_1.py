import pandas as pd
import numpy as np
import glob
import os

from autograder_base import Base_Autograder
from autograder_project_1 import Autograder_1_2

# Colors for console printing,
W = '\033[0m'   # white (normal)
R = '\033[31m'  # red
O = '\033[33m'  # orange
Y = '\033[93m'  # yellow
G = '\033[32m'  # green


class Group_Autograder_1(Base_Autograder):

    def __init__(self):
        super().__init__()
        self.DEBUG = True

        # Directory information
        self.test_dir = os.path.abspath("test_data")
        self.submission_dir = "./submissions/"

        # Test information
        self.test_names = [
            "P2-1",
            "P2-2",
            "P2-3"
        ]

        # Files to print results to
        self.grade_file = "results_grades.csv"
        self.time_file =  "results_times.csv"

    # Flatten directory
    def flatten(self, directory):
        for path in os.listdir(directory):
            for subpath in os.listdir(directory + "/" + path):
                command = "(mv {src} {tgt})".format(
                    src = directory + "/" + path + "/" + subpath,
                    tgt = directory
                )
                os.system(command)

    def autograde(self):
        return



"""
Start of program logic
"""
if __name__ == "__main__":

    group = Group_Autograder_1()
    grades, times = group.autograde()

    # print results to csv
    grades.to_csv(group.grade_file)
    times.to_csv(group.time_file)