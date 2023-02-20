from termcolor import colored
import numpy as np
import os
import pandas as pd
import sys

# Tell the script where to find the base autograder
sys.path.append(os.path.join("..", ".."))
from autograder_base import Base_Autograder


class Autograder_3_2(Base_Autograder):

    def __init__(self):
        super().__init__()

        # Student information
        self.student_name = "student"
        self.is_grad = True

        # Directory information
        self.this_dir =          "."
        self.student_files =     "Problem_2"
        self.test_in_files =     os.path.join("..", "test_data", "DNA_Files")
        self.test_out_files =    os.path.join("..", "test_data", "Problem_2")

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
        this_dir =      os.path.abspath(self.this_dir)
        test_in_dir =   os.path.abspath(self.test_in_files)
        test_out_dir =  os.path.abspath(self.test_out_files)

        # Print the test dir and project dir
        if self.DEBUG:
            print(colored(f" --> Test dir: {test_in_dir}", "green"))
            print(colored(f" --> Project dir: {this_dir}", "green"))

        # get num cols for threads
        columns = []
        for file in self.test_names:
            for program in file:
                for i in range(len(self.threads)):
                    columns.append(f"{program[0]}-T{self.threads[i]}")

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

        # Input RNA files
        t_rna = [
            os.path.join(test_in_dir, "GRCh38_50_rna.fna"),
            os.path.join(test_in_dir, "GRCh38_reduced_rna.fna"),
            os.path.join(test_in_dir, "GRCh38_latest_rna.fna")
        ]

        # The expected output files
        t_out = [
            os.path.join(test_out_dir, "p2_output_50.csv"),
            os.path.join(test_out_dir, "p2_output_reduced.csv"),
            os.path.join(test_out_dir, "p2_output_latest.csv")
        ]

        # The actual output from the student
        t_dir = os.path.join(this_dir, self.student_files)
        t_p2_prefix = ["critical", "atomic", "locks", "schedule"]
        t_p2_get = [
            [[], [], [], [], []],   # 50
            [[], [], [], [], []],   # reduced
            [[], [], [], [], []]    # latest
        ]
        t_p2_tim = [
            [[], [], [], [], []],   # 50
            [[], [], [], [], []],   # reduced
            [[], [], [], [], []]    # latest
        ]
        rna = ["50", "reduced", "latest"]
        for out in range(len(t_out)):
            for pre in range(len(t_p2_prefix)):
                for t in self.threads:
                    t_p2_get[out][pre].append(
                        os.path.join(t_dir, f"res_{t_p2_prefix[pre]}_{rna[out]}_{t}th.csv")
                    )
                    t_p2_tim[out][pre].append(
                        os.path.join(t_dir, f"tim_{t_p2_prefix[pre]}_{rna[out]}_{t}th.csv")
                    )
                    

        # For each problem, generate commands to make and run the test cases
        #   generate the commands to run the tests here
        c_p2 = [
            [[], [], [], [], []],   # 50
            [[], [], [], [], []],   # reduced
            [[], [], [], [], []]    # latest
        ]

        # Alternate program names, if needed
        p2_names = [
            "compute_average_TF_Exp1_critical",
            "compute_average_TF_Exp1_atomic",
            "compute_average_TF_Exp1_locks",
            "compute_average_TF_Exp2_schedule",
        ]

        # Generate the problems' command-variables
        for file in range(len(t_rna)):            # For RNA input
            for program in range(len(p2_names)):  # For program
                for t in range(len(self.threads)):     # For num thread counts
                    c_p2[file][program].append([
                        p2_names[program],           # program type, like locks or sharing
                        t_rna[file],                 # input file
                        t_p2_get[file][program][t],  # resulting output file
                        t_p2_tim[file][program][t],  # resulting time file
                        self.threads[t]                   # num threads
                    ])

        #  we have everything we need to test a problem now
        #   grade each individual problem here!
        # TA) TODO: specify each problem's test parameters
        # Problem 2
        test_params = [
            [[], [], [], [], []],   # 50
            [[], [], [], [], []],   # reduced
            [[], [], [], [], []]    # latest
        ]
        for file in range(len(t_rna)):            # For RNA input
            for program in range(len(p2_names)):  # For program names
                for t in range(len(self.threads)):     # For num thread counts
                    test_params[file][program].append(
                        [t_dir, t_out[file], t_p2_get[file][program][t], c_p2[file][program][t], False]
                    )

        # testing results
        test_results = [None] * len(columns)
        time_results = [None] * len(columns)

        # test every problem in a loop
        grade_index = 0
        for file in range(len(self.test_names)):
            for program in range(len(self.test_names[file])):
                for thread in range(len(self.threads)):
                    params = test_params[file][program][thread]
                    result = self.grade_problem(
                        params[0],  # Problem dir
                        params[1],  # Expected outputs of test i
                        params[2],  # Output file names
                        [params[3]],  # Command for getting test i results
                        params[4]   # Whether to let the differences have an error range
                    )

                    # set results
                    test_results[grade_index] = result[0]
                    time_results[grade_index] = result[1]

                    # add each result to the dataframes
                    grade.loc[self.student_name, columns[grade_index]] = test_results[grade_index][0]
                    time.loc [self.student_name, columns[grade_index]] = time_results[grade_index][0]
                    grade_index = grade_index + 1


        return [grade, time]


def main():
    print(colored("Autograding for Project 3 Problem 2:\n", "green"))
    
    p2 = Autograder_3_2()
    res = p2.autograde()

    total   = len(res[0].columns)
    correct = int(res[0].sum(axis=1)[0])

    print(colored("\nFinal Grades:", "yellow"))
    res[0].to_csv("P3_2_grades.csv")
    print(res[0])

    print(colored("\nFinal Timings:", "yellow"))
    res[1].to_csv("P3_2_times.csv")
    print(res[1])

    print(colored(f"\n --> {correct}/{total} problems correct\n"))


if __name__ == "__main__":
    main()