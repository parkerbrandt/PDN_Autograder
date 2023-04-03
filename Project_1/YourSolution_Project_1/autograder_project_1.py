import numpy as np
import os
import pandas as pd
import sys

# Tell the script where to find the base autograder
sys.path.append("..")
sys.path.append(os.path.join("..", ".."))
from autograder_base import Base_Autograder

# Colors
W = '\033[0m'  # white (normal)
R = '\033[31m'  # red
O = '\033[33m'  # orange
Y = '\033[93m'  # yellow
G = '\033[32m'  # green


class Autograder_1_2(Base_Autograder):

    def __init__(self, in_student_name="student", in_this_dir=".", in_test_files=["..", "test_data"]):
        super().__init__()

        # Student information
        self.student_name = in_student_name
        self.is_grad = True
        self.DEBUG = True

        # Directory information
        self.this_dir =         in_this_dir
        self.student_files =    "Problem_2"
        self.test_files =       ""

        for i in range(len(in_test_files)):
            self.test_files = os.path.join(self.test_files, in_test_files[i])
    
        self.test_files = os.path.join(self.test_files, "Problem_2")

        # Test information
        self.test_names = [
            "P2-1",
            "P2-2",
            "P2-3"
        ]


    def autograde(self):
        return
    

if __name__ == "__main__":

    p1 = Autograder_1_2()

