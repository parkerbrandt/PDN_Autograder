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
Project 2, Problem 3 Autograder
"""
class Autograder_2_3(Base_Autograder):

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
        self.student_files =    "Problem_3"
        self.test_files =       ""

        for i in range(len(in_test_files)):
            self.test_files =    os.path.join(self.test_files, in_test_files[i])

        self.test_files =    os.path.join(self.test_files, "Problem_3")

        # Test information
        self.threads = [2, 4, 8]
        self.test_names = [
            "P3-1"
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
    Autogrades Problem 3
    """
    def autograde(self):
        
        this_dir = os.path.abspath(self.this_dir)
        test_dir = os.path.abspath(self.test_files)

        # Print the test dir and project dir
        if self.DEBUG:
            print(f"{G} --> Test dir: {test_dir}{W}")
            print(f"{G} --> Project dir: {this_dir}{W}")

        columns = []
        for p in self.test_names:
            columns.append(f"{p}")

        # student grades
        grade = pd.DataFrame(
            np.nan,
            index=[self.student_name],
            columns=columns
        )

        # student timing
        time = pd.DataFrame(
            np.nan,
            index=[self.student_name],
            columns=columns
        )

        # Input files

        # Expected output files
        t_out = [

        ]

        # Actual output files
        t_dir = []
        t_get = []

        c_p3 = []

        for file in range(len(self.test_names)):
            c_p3.append([

            ])

        c_p3_ref = {}

        # Autograde with test parameters
        test_params = []

        for file in range(len(self.test_names)):
            test_params.append(
                [t_dir, t_out[file], t_get[file], c_p3[file], False, self.is_error_within_bound]
            )

        test_results = [None] * len(columns)

        # Test every problem
        grade_index = 0
        for file in range(len(self.test_names)):
            params = test_params[file]
            result = self.grade_problem(
                params[0],                      # student directory
                [params[1]],                    # test output
                [params[2]],                    # test results
                [params[3]],                    # commands
                c_p3_ref,                       # command references
                params[4],                      # exact
                params[5]                       # error function to be passed
            )

            test_results[grade_index] = result[0]

            # Add results to dataframes
            grade.loc[self.student_name, columns[grade_index]] = test_results[grade_index][0]
            grade_index += 1

        return [grade, time]
        

def main():
    print(f"{G}Autograding for Project 2 Problem 3:\n{W}")
    
    p3 = Autograder_2_3()
    res = p3.autograde()

    total   = len(res[0].columns)
    correct = int(res[0].sum(axis=1)[0])

    print(f"{Y}\nFinal Grades:{W}")
    res[0].to_csv("P2_3_grades.csv")
    print(res[0])

    print(f"{Y}\nFinal Timings:{W}")
    res[1].to_csv("P2_3_times.csv")
    print(res[1])

    print((f"\n --> {correct}/{total} problems correct\n"))


if __name__ == "__main__":
    main()