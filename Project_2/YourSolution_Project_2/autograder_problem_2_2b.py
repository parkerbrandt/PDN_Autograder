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


"""
Project 2, Problem 2b Autograder

Autogrades a single student's code
"""
class Autograder_2_2b(Base_Autograder):

    """
    Initializes variables
    """
    def __init__(self, in_student_name="student", in_this_dir=".", in_test_files=["..", "test_data"]):
        super().__init__()

        # Student information
        self.student_name = in_student_name
        self.is_grad = True
        self.DEBUG = True

        # Directory information
        self.this_dir =         in_this_dir
        self.student_files =    "Problem_2"
        self.test_in_files =    ""
        self.test_out_files =   ""

        for i in range(len(in_test_files)):
            self.test_in_files =    os.path.join(self.test_in_files, in_test_files[i])
            self.test_out_files =   os.path.join(self.test_out_files, in_test_files[i])

        self.test_in_files =    os.path.join(self.test_in_files, "Input_Matricies_Prob_1_And_2")
        self.test_out_files =   os.path.join(self.test_out_files, "Problem_2B")

        # Test information
        self.threads = [2, 4, 8]
        self.test_names = [
            ""
        ]


    """
    Check if the student's answer is within a reasonable bound of the actual answer
    Error Bound:
        - Check that student's answer is within 1% of actual answer

    Parameters:
        - expected  (ndarray):  The actual answer read from test_data/
        - result    (ndarray):  The student's answer
    """
    def is_error_within_bound(self, expected, result):

        try:
            # Make sure the shapes of the 
            if expected.shape != result.shape:
                raise Exception("Shapes of expected output and student output do not match")
            
            # Compare the two arrays
            return np.array_equal(expected, result, equal_nan=True)

        except Exception as err:
            print(f"{R}Error reading output file:{W}")
            print(f"{R}\t{err}{W}")

        return


    """
    Autogrades Problem 2a
    Overrides Base_Autograder.autograde()

    Constructs a test by retrieving data about paths and data locations, then calls Base_Autograder.grade_problem()
    to test and grade the problem
    """
    def autograde(self):
        return
        

"""
Start of Program Logic
"""
def main():
    print(f"{G}Autograding for Project 2 Problem 2b:\n{W}")
    
    p2 = Autograder_2_2b()
    res = p2.autograde()

    total   = len(res[0].columns)
    correct = int(res[0].sum(axis=1)[0])

    print(f"{Y}\nFinal Grades:{W}")
    res[0].to_csv("P2_2b_grades.csv")
    print(res[0])

    print(f"{Y}\nFinal Timings:{W}")
    res[1].to_csv("P2_2b_times.csv")
    print(res[1])

    print((f"\n --> {correct}/{total} problems correct\n"))


if __name__ == "__main__":
    main()