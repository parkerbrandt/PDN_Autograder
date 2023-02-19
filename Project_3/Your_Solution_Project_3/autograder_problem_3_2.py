from autograder_base import grade_problem, Base_Autograder
from termcolor import colored
import numpy as np
import os
import pandas as pd


class Autograder_3_2(Base_Autograder):

    def __init__(self):
        super().__init__()

        # Student information
        self.student_name = "student"
        self.is_grad = True

        # Directory information
        self.student_files =     os.path.join(".", "Problem_2")
        self.test_in_files =     os.path.join("..", "test_data", "DNA_Files")
        self.test_out_files =    os.path.join("..", "test_data", "Problem_2")
        self.this_dir =          os.path.join(".")

        # Test information
        self.threads = [8]
        self.test_names = [
            # 50 items
            [
                ["P2-50-critical"],   # critical
                ["P2-50-atomic"],     # atomic
                ["P2-50-locks"],      # locks
                ["P2-50-schedule"]    # schedule
            ],

            # Reduced items
            [
                ["P2-Reduced-critical"],   # critical
                ["P2-Reduced-atomic"],     # atomic
                ["P2-Reduced-locks"],      # locks
                ["P2-Reduced-schedule"]    # schedule
            ],

            # All items
            [
                ["P2-Latest-critical"],   # critical
                ["P2-Latest-atomic"],     # atomic
                ["P2-Latest-locks"],      # locks
                ["P2-Latest-schedule"]    # schedule
            ]
        ]

    def autograde(self):
        this_dir = os.path.abspath(self.this_dir)
        test_in_dir = os.path.abspath(self.test_in_files)
        test_out_dir = os.path.abspath(self.test_out_files)

        # Print the test dir and project dir
        if self.DEBUG:
            print(colored(f" --> Test dir: {test_in_dir}", "green"))
            print(colored(f" --> Project dir: {this_dir}", "green"))

        # get num cols for threads
        columns = []
        for file in self.test_names:
            for program in file:
                for i in range(len(self.threads)):
                    columns.append(program[0] + "-T" + str(self.threads[i]))

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

        

        return [grade, time]


def main():

    print(colored("Autograding for Project 3 Problem 2:\n", "green"))
    
    p2 = Autograder_3_2()
    res = p2.autograde()

    total   = str(len(res[0].columns))
    correct = str(int(res[0].sum(axis=1)[0]))

    print(colored("\nFinal Grades:", "yellow"))
    res[0].to_csv("P3_2_grades.csv")
    print(res[0])

    print(colored("\nFinal Timings:", "yellow"))
    res[1].to_csv("P3_2_times.csv")
    print(res[1])

    print(colored(f"\n --> {correct}/{total} problems correct\n"))


if __name__ == "__main__":
    main()