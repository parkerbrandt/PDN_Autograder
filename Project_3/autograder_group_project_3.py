import autograding_individual_3a as autograding
import pandas as pd
import numpy as np
import glob
import os

# To get debug messages
DEBUG = True

# Colors for console printing,
W = '\033[0m'   # white (normal)
R = '\033[31m'  # red
O = '\033[33m'  # orange
Y = '\033[93m'  # yellow
G = '\033[32m'  # green


"""
    ~~~~~~~~~~~~~~~~~ Project 2   ver 2a ~~~~~~~~~~~~~~~~~
    This file is used to autograde a .zip file of student submissions.
    To run this, do the following:
        1) Note the folder that contains this file. [autograding_group.py]
        2) Place the individual autograder .py script into this folder.
            2.1) You may rename the individual grading file above. [autograding_individual_2a.py]
        3) Create a folder called "submissions" and put any zipped solutions into this folder.
            3.1) You may rename the submission folder below.
            3.2) .zip files expect name such as "ShawJes_HW1.zip"
        4) Create a folder called "test_data" and the testing files into this folder.
            4.1) You may rename the folder below.
        5) Run this file, and you will receive the results.
            5.1) To let students autograde their solutions, give them the individual grading file only.
            
    Run this file with: "python3 autograding_group.py" OR "python autograding_group.py"
        On Schooner, you may need to use "module load numpy", etc., then the python command again.
        
    >> Make sure you have the structure below!:
    this_dir/         [.] 
        autograding_group.py   <--- Place here.
        test_data/    
        submissions/
            ShawJes_HW/
            WalkerDoug_HW/
            ...
            
    Note: TA) TODO: indicates places that should be changed when assignments are modified
"""

# TA) TODO: change based on assignment needs
# these are the column names for the test/time results
test_names = [
    "P1-T1",  "P1-T2",  "P1-T3",  "P1-T4",
    "P2a-T1", "P2a-T2", "P2a-T3", "P2a-T4",
    "P2b-T1", "P2b-T2", "P2b-T3", "P2b-T4",
    "P3-T1",  "P3-T2",
    "P4-T1"
]

# files to print the results to
grade_file = 'results_grades.csv'
time_file  = 'results_times.csv'

# this is to be passed to the individual grader
#   i do not think we can tell this with a blended canvas course
#   so, change this variable if needed
#   (when false, less problems are graded)
is_grad = True

# directories to use
test_dir        = "./test_data/"
submissions_dir = "./submissions/"


# ----------------
# get the zipped files
unzipped_files = glob.glob(submissions_dir + '*.zip')


# -----------------------------
# unzip each student's zip file
for file in unzipped_files:
    # get the student names from each zip file
    # e.g. ShawJes
    dir_file_name = file.split('_')[0]
    if DEBUG:
        print(G + file + W)

    # unzip the file into a folder with their name
    command = "(unzip {} -d {})".format(file, dir_file_name)
    os.system(command)

# unzipped directories
directories = glob.glob(submissions_dir + '*/')  # these are the students' dirs


# --------------------------------------------------------------
# get student names and create a dataframe to store their grades
student_names = [d.split('/')[2] for d in directories]
grades = pd.DataFrame(
    np.nan,
    index   = [],
    columns = [i for i in test_names]
)
times = pd.DataFrame(
    np.nan,
    index   = [],
    columns = [i for i in test_names]
)


# ------------------
# grade each student
for i in range(len(directories)):
    try:
        # run the individual autograder on the student
        res = autograding.autograde(
            os.path.abspath(directories[i]),
            os.path.abspath(test_dir),
            student_names[i],
            is_grad
        )

        # add results to dataframes
        grades = grades.append(res[0])
        times  = times.append(res[1])

        if DEBUG:
            print(Y + "\n Final grades:" + W)
            print(res[0])

            print(Y + "\n Final timings:" + W)
            print(res[1])

    # catch any weird stuff
    except Exception as err:
        print('\n' + R + "Error grading for " + student_names[i])
        print(Y + str(err) + W)

# show results
print('\n', grades)

# print results to csv
grades.to_csv(grade_file)
times.to_csv(time_file)
