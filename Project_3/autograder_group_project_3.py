import pandas as pd
import numpy as np
import glob
import os

from autograder_base import Base_Autograder
from autograder_problem_3_2 import Autograder_3_2
from autograder_problem_3_3 import Autograder_3_3
from autograder_problem_3_4 import Autograder_3_4

# Colors for console printing,
W = '\033[0m'   # white (normal)
R = '\033[31m'  # red
O = '\033[33m'  # orange
Y = '\033[93m'  # yellow
G = '\033[32m'  # green


class Group_Autograder_3(Base_Autograder):

    def __init__(self):
        super().__init__()

        # Directories
        self.test_dir = os.path.abspath("test_data")
        self.submissions_dir = os.path.abspath("submissions")
        
        # Column names for the test/time results
        self.test_names = [
            "P1-T1",  "P1-T2",  "P1-T3",  "P1-T4",
            "P2a-T1", "P2a-T2", "P2a-T3", "P2a-T4",
            "P2b-T1", "P2b-T2", "P2b-T3", "P2b-T4",
            "P3-T1",  "P3-T2",
            "P4-T1"
        ]

        # files to print the results to
        self.grade_file = 'results_grades.csv'
        self.time_file  = 'results_times.csv'

        self.DEBUG = True


    def autograde(self):
        # get the zipped files
        unzipped_files = glob.glob(self.submissions_dir + '*.zip')

        # unzip each student's zip file
        for file in unzipped_files:
            # get the student names from each zip file
            # e.g. ShawJes
            dir_file_name = file.split('_')[0]
            if self.DEBUG:
                print(G + file + W)

            # unzip the file into a folder with their name
            command = "(unzip {} -d {})".format(file, dir_file_name)
            os.system(command)

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

        # grade each student
        for i in range(len(directories)):
            try:
                # run the individual autograder on the student
                p2 = Autograder_3_2(student_names[i], directories[i], ["..", "..", "test_data"])
                p3 = Autograder_3_3(student_names[i], directories[i], ["..", "..", "test_data"])
                p4 = Autograder_3_4(student_names[i], directories[i], ["..", "..", "test_data"])

                res2 = p2.autograde()
                res3 = p3.autograde()
                res4 = p4.autograde()

                # res = autograding.autograde(
                #     os.path.abspath(directories[i]),
                #     os.path.abspath(self.test_dir),
                #     student_names[i]
                # )

                res = res2[0].append(res3[0])
                res = res.append(res4[0])
                
                t_res = res2[1].append(res3[1])
                t_res = t_res.append(res4[1])

                # add results to dataframes
                grades = grades.append(res)
                times  = times.append(t_res)

                if self.DEBUG:
                    print(f"{Y}\nFinal grades: {W}")
                    print(res[0])

                    print(f"{Y}\nFinal timings: {W}")
                    print(res[1])

            # catch any weird stuff
            except Exception as err:
                print(f"\n{R}Error grading for {student_names[i]}")
                print(f"{Y}{err}{W}")

        return grades, times
    

"""
Start of program logic
"""
if __name__ == "__main__":

    group = Group_Autograder_3()
    grades, times = group.autograde()

    # print results to csv
    grades.to_csv(group.grade_file)
    times.to_csv(group.time_file)