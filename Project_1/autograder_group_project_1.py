import pandas as pd
import numpy as np
import glob
import os
import sys

# Tell the script where to find the base autograder
sys.path.append("..")
sys.path.append(os.path.join("..", ".."))
from autograder_base import Base_Autograder
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
        # get the zipped files
        unzipped_files = glob.glob(self.submissions_dir + '*.zip')
        print(unzipped_files)

        # unzip each student's zip file
        for file in unzipped_files:
            # get the student names from each zip file
            # e.g. ShawJes
            dir_file_name = file.split('_')[0]
            if self.DEBUG:
                print(f"{G}{file}{W}")

            # unzip the file into a folder with their name
            command = "(unzip {} -d {})".format(file, dir_file_name)
            os.system(command)

            # Fix zip if directories aren't correct
            if len(next(os.walk(dir_file_name))[1]) > 1:
                self.flatten(dir_file_name)

        # unzipped directories
        directories = glob.glob(self.submissions_dir + '*/')  # these are the students' dirs

        # get student names and create a dataframe to store their grades
        student_names = [d.split('/')[2] for d in directories]
        grades = pd.DataFrame(
            np.nan,
            index   = [],
            columns = [i for i in self.test_names]
        )
        times = pd.DataFrame(
            np.nan,
            index   = [],
            columns = [i for i in self.test_names]
        )


        # Grade each student
        for i in range(len(directories)):
            try:
                p2 = Autograder_1_2(student_names[i], directories[i], ["..", "..", "test_data"])
                res2 = p2.autograde()

                grades = grades.append(res2[0])
                times = times.append(res2[1])

                if self.DEBUG:
                    print(f"{Y}\nFinal grades: {W}")
                    print(res2[0])

                    print(f"{Y}\nFinal timings: {W}")
                    print(res2[1])
            
            except Exception as err:
                print(f"\n{R}Error grading for {student_names[i]}")
                print(f"{Y}{err}{W}")

        return grades, times



"""
Start of program logic
"""
if __name__ == "__main__":

    group = Group_Autograder_1()
    grades, times = group.autograde()

    # print results to csv
    grades.to_csv(group.grade_file)
    times.to_csv(group.time_file)