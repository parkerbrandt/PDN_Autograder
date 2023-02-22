import pandas as pd
import numpy as np
import filecmp
import os
import platform
import re
from termcolor import colored
from abc import ABC, abstractclassmethod


"""
* 
* Autograder Base
* Contains common functions across all autograding scripts to be called
* Functions:
*       - gen_filenames()
*       - grade_problem()
*       - autograde()
*
"""

class Base_Autograder(ABC):

    def __init__(self):
        self.DEBUG = True
        return

    # generate file names from a given template
    # FORMAT LIKE THIS: "test_{index}.txt"
    def gen_filenames(self, template, n):
        filenames = []
        for i in range(1, n + 1):
            filename = template.format(index=i)
            filenames.append(filename)
        return filenames

    # this will take a problem, run the student code, then compare with
    #   expected output. it will return the points earned
    def grade_problem(self, student_dir, t_output, t_res, commands, exact):
        # how many tests to run
        n = len(commands)

        # array of scores to return
        scores = []
        for i in range(n):
            scores.append(0)

        # array of times to return
        times = []
        for i in range(n):
            times.append(-1)

        # try to make and run the code
        try:
            # alert what directory doesn't have a makefile (dont copy it)
            if not os.path.isfile(os.path.join(student_dir, "Makefile")):
                print(colored(f"\nERROR: Missing Makefile when trying to test in {student_dir}!", "red"))
                print(colored(f"       Skipping testing for {commands[0][0]}...", "red"))
                return [scores, times]

            # run makefile
            command = f"(cd {student_dir} && make)"
            err = os.system(command)
            if err != 0:
                print(colored(f"Error making the program {commands[0][0]}", "red"))
                return [scores, times]

            # run and analyze the problem
            for i in range(0, n):

                print(colored(f"Testing for {commands[i][0]}'s output: {t_res[i]}", "green"))

                # generate the command and run the program
                #   ex. ./Problem_1/parallel_mult_mat_mat in.csv 10 10 ...
                command = f"(cd {student_dir} && ./{str(commands[i][0])}"
                if platform.system() == "Windows":
                    command = command.replace('/', '\\')
                for j in range(1, len(commands[0]) - 1):
                    command = f"{command} {str(commands[i][j])}"
                command = f"{command} {str(commands[i][-1])})"
                print(command)
                err = os.system(command)

                # skip over if cant run the program...
                if err != 0:
                    print(colored(f"\nError running the program {commands[i][0]}", "red"))
                    continue

                # get data from csv result and expected outputs
                try:
                    result = np.genfromtxt(os.path.join(student_dir, t_res[i]), delimiter=",", dtype=float, encoding='ISO-8859-1')
                except Exception as err:
                    print(colored(f"Error finding program's output file: {os.path.join(student_dir, t_res[i])}", "red"))
                    print(colored(f"{err}", "yellow"))
                    continue

                try:
                    expected = np.genfromtxt(t_output[i], delimiter=",", dtype=float, encoding='ISO-8859-1')
                except Exception as err:
                    print(colored(f"Error finding the expected output file: ", "red"))
                    print(colored(f"{err}", "yellow"))
                    continue

                # compare file dims
                matches = False
                if False:
                    print(colored(f"Output file {t_output[i]}'s dimensions are different from expected result's!", "red"))
                    continue

                # compare the files by simply looking at the text
                elif exact:
                    if self.DEBUG:
                        print(colored(f"Testing exact values...", "yellow"))
                    matches = filecmp.cmp(
                        t_output[i],
                        os.path.join(student_dir, t_res[i]),
                        shallow=False
                    )

                # compare by considering value-errors
                else:
                    if self.DEBUG:
                        print(colored(f"Testing approximate values...", "yellow"))
                    diff = np.sum(np.absolute(expected - result))
                    diff = diff / np.ravel(expected).shape[0]
                    print(colored(f"DIFF: {diff}", "red"))
                    if diff < 0.1:
                        matches = True

                if not matches:
                    print(colored(f"TRY AGAIN", "red"))
                    # if there is an error running the command,
                    #   try placing the num_threads at the end
                    command = f"(cd {student_dir} && ./{commands[i][0]}"
                    if platform.system() == "Windows":
                        command = command.replace('/', '\\')
                    for j in range(1, len(commands[0]) - 3):
                        command = f"{command} {commands[i][j]}"
                    command = f"{command} {commands[i][-2]}"
                    command = f"{command} {commands[i][-1]}"
                    command = f"{command} {commands[i][-3]})"
                    err = os.system(command)

                    # skip over if cant run the program...
                    if err != 0:
                        print(colored(f"Error running the program {commands[i][0]}", "red"))
                        continue

                    # get data from csv result and expected outputs
                    try:
                        result = np.genfromtxt(os.path.join(student_dir, t_res[i]), delimiter=",", dtype=float, encoding='ISO-8859-1')
                    except Exception as err:
                        print(colored(f"Error finding program's output file: {os.path.join(student_dir, t_res[i])}", "red"))
                        print(colored(f"{err}", "yellow"))
                        continue

                    try:
                        expected = np.genfromtxt(t_output[i], delimiter=",", dtype=float, encoding='ISO-8859-1')
                    except Exception as err:
                        print(colored(f"Error finding the expected output file: {t_output[i]}", "red"))
                        print(colored(f"{err}", "yellow"))
                        continue

                    # compare file dims
                    matches = False
                    if False: #expected.shape != result.shape:
                        print(colored(f"Output file {t_output[i]}'s dimensions are different from expected result's!", "red"))
                        continue


                    # compare the files by simply looking at the text
                    elif exact:
                        if self.DEBUG:
                            print(colored(f"Testing exact values...", "yellow"))
                        matches = filecmp.cmp(
                            t_output[i],
                            os.path.join(student_dir, t_res[i]),
                            shallow=False
                        )

                    # compare by considering value-errors
                    else:
                        if self.DEBUG:
                            print(colored(f"Testing approximate values...", "yellow"))
                        diff = np.sum(np.absolute(expected - result))
                        diff = diff / np.ravel(expected).shape[0]
                        print(colored(f"DIFF: {diff}", "red"))
                        if diff < 0.1:
                            matches = True


                # give final score
                if matches:
                    scores[i] = 1
                else:
                    if self.DEBUG:
                        print(colored(f"The expected output: {t_output[i]} does not match the result!", "red"))

                try:
                    t = np.genfromtxt(os.path.join(student_dir, commands[i][-1]), delimiter=',')
                except Exception as err:
                    print(colored(f"Error finding program's time file: {commands[i][-1]}", "red"))
                    continue
                times[i] = t

                if self.DEBUG:
                    print(colored(f"    Test result {i} = {scores[i]}", "yellow"))
                    print(colored(f"    Time result {i} = {times[i]}s\n", "yellow"))

        # catch the weird stuff
        except Exception as err:
            print(colored(f"\nUnexpected error!", "red"))
            print(colored(f"{err}", "yellow"))

        return [scores, times]

    @abstractclassmethod
    def autograde(self):
        pass