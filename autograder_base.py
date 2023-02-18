import pandas as pd
import numpy as np
import filecmp
import os
import platform
import re

# To get debug messages
DEBUG = True

# Colors for console printing,
W = '\033[0m'  # white (normal)
R = '\033[31m'  # red
O = '\033[33m'  # orange
Y = '\033[93m'  # yellow
G = '\033[32m'  # green

# -----------------------------------------
# generate file names from a given template
# FORMAT LIKE THIS: "test_{index}.txt"
def gen_filenames(template, n):
    filenames = []
    for i in range(1, n + 1):
        filename = template.format(index=i)
        filenames.append(filename)
    return filenames

# -----------------------------------------------------------------
# this will take a problem, run the student code, then compare with
#   expected output. it will return the points earned
def grade_problem(student_dir, t_output, t_res, commands, exact):
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
            print(f"\n{R}ERROR: Missing Makefile when trying to test in {student_dir}! {W}")
            print(f"{R}       Skipping testing for {commands[0][0]}...{W}")
            return [scores, times]

        # run makefile
        command = f"(cd {student_dir} && make)"
        err = os.system(command)
        if err != 0:
            print(f"{R}Error making the program {commands[0][0]}{W}")
            return [scores, times]

        # run and analyze the problem
        for i in range(0, n):

            print(f"{G}Testing for {commands[i][0]}'s output: {t_res[i]}{W}")

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
                print(f"{R}\nError running the program {commands[i][0]}{W}")
                continue

            # get data from csv result and expected outputs
            try:
                result = np.genfromtxt(os.path.join(student_dir, t_res[i]), delimiter=",", dtype=float, encoding='ISO-8859-1')
            except Exception as err:
                print(f"{R}Error finding program's output file: {os.path.join(student_dir, t_res[i])}")
                print(f"{O}{err}{W}")
                continue

            try:
                expected = np.genfromtxt(t_output[i], delimiter=",", dtype=float, encoding='ISO-8859-1')
            except Exception as err:
                print(f"{R}Error finding the expected output file: ")
                print(f"{O}{err}{W}")
                continue

            # compare file dims
            matches = False
            if False:
                print(f"{R}Output file {t_output[i]}'s dimensions are different from expected result's!{W}")
                continue

            # compare the files by simply looking at the text
            elif exact:
                if DEBUG:
                    print(f"{O}Testing exact values...{W}")
                matches = filecmp.cmp(
                    t_output[i],
                    os.path.join(student_dir, t_res[i]),
                    shallow=False
                )

            # compare by considering value-errors
            else:
                if DEBUG:
                    print(f"{O}Testing approximate values...{W}")
                diff = np.sum(np.absolute(expected - result))
                diff = diff / np.ravel(expected).shape[0]
                print(f"{R}DIFF: {diff}{W}")
                if diff < 0.1:
                    matches = True

            if not matches:
                print(f"{R}TRY AGAIN{W}")
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
                    print(f"{R}Error running the program {commands[i][0]}{W}")
                    continue

                # get data from csv result and expected outputs
                try:
                    result = np.genfromtxt(os.path.join(student_dir, t_res[i]), delimiter=",", dtype=float, encoding='ISO-8859-1')
                except Exception as err:
                    print(f"{R}Error finding program's output file: {os.path.join(student_dir, t_res[i])}")
                    print(f"{O}{err}{W}")
                    continue

                try:
                    expected = np.genfromtxt(t_output[i], delimiter=",", dtype=float, encoding='ISO-8859-1')
                except Exception as err:
                    print(f"{R}Error finding the expected output file: {t_output[i]}")
                    print(f"{O}{err}{W}")
                    continue

                # compare file dims
                matches = False
                if False: #expected.shape != result.shape:
                    print(f"{R}Output file {t_output[i]}'s dimensions are different from expected result's!{W}")
                    continue


                # compare the files by simply looking at the text
                elif exact:
                    if DEBUG:
                        print(f"{O}Testing exact values...{W}")
                    matches = filecmp.cmp(
                        t_output[i],
                        os.path.join(student_dir, t_res[i]),
                        shallow=False
                    )

                # compare by considering value-errors
                else:
                    if DEBUG:
                        print(f"{O}Testing approximate values...{W}")
                    diff = np.sum(np.absolute(expected - result))
                    diff = diff / np.ravel(expected).shape[0]
                    print(f"{R}DIFF: {diff}{W}")
                    if diff < 0.1:
                        matches = True


            # give final score
            if matches:
                scores[i] = 1
            else:
                if DEBUG:
                    print(f"{R}The expected output: {t_output[i]} does not match the result!{W}")

            try:
                t = np.genfromtxt(os.path.join(student_dir, commands[i][-1]), delimiter=',')
            except Exception as err:
                print(f"{R}Error finding program's time file: {commands[i][-1]}{W}")
                continue
            times[i] = t

            if DEBUG:
                print(f"{Y}    Test result {i} = {scores[i]}")
                print(f"{Y}    Time result {i} = {times[i]}s\n{W}")

    # catch the weird stuff
    except Exception as err:
        print(f"\n{R}Unexpected error!")
        print(f"{Y}{err}{W}")

    return [scores, times]

# ------------------------------------------
# this will autograde one project submission
def autograde(in_this_dir, in_test_dir, in_student_name, num_problems, test_names={}, test_info={}, in_is_grad=False):
    # for mass grading purposes, ignore if individually grading
    #   getting the abs path resolves some issues...
    this_dir = os.path.abspath(in_this_dir)
    test_dir = os.path.abspath(in_test_dir)
    student_name = in_student_name
    is_grad = in_is_grad

    # Print the test dir and project dir
    if DEBUG:
        print(f"{G} --> Test dir: {test_dir} {W}")
        print(f"{G} --> Project dir: {this_dir} {W}")

    # student grade
    grade = pd.DataFrame(
        np.nan,
        index=[student_name],
        columns=[i for i in test_names]
    )

    # student timing
    time = pd.DataFrame(
        np.nan,
        index=[student_name],
        columns=[i for i in test_names]
    )

    # TODO: Iterate through each directory in test_dir, then perform the tests
    # test_locations format: key = test name, value = [Input Dir, Output Dir] or value = [Input & Output Dir]

    # t_dir = problem directory
    # t_out = expected output
    # t_get = program result
    # t_tim = program time

    for test_name, info in test_info.items():

        prob_num = test_name[1:]

        # Reading in input
        t_dir = os.path.join(test_dir, info[1])

        t_in = []
        for i in range(0, len(info)-1):
            t_in[i] = gen_filenames(t_dir, )

        # Output Files
        t_dir = os.path.join(test_dir, info[-1])
        t_out = gen_filenames(os.path.join(t_dir, "test{index}_output.csv"), len(info)-1)
        t_get = gen_filenames("test_{index}_out.csv", len(info)-1)
        t_tim = gen_filenames("test_{index}_out_time.csv", len(info)-1)
        
        for test in test_names[test_name]:
            # Execute command
            command = [
                info[0],
            ]
















    # TA) TODO: add the correct test files for every problem
    #  each problem will have its own set of test files
    #   list the test file names for each problem here
    #   NOTE: the test files have special directories, so we have to specify them here
    # t_dir = test_dir + "/Input_Matricies_Prob_1_And_2/"
    t_dir = os.path.join(test_dir, "Input_Matricies_Prob_1_And_2")
    t_mat_a = gen_filenames(os.path.join(t_dir, "test{index}_input_mat_a.csv"), 4)  # Input matrices
    t_mat_b = gen_filenames(os.path.join(t_dir, "test{index}_input_mat_b.csv"), 4)  #

    # Problem 1
    t_dir = os.path.join(test_dir, "Problem_1")
    t_p1_out = gen_filenames(os.path.join(t_dir, "test{index}_output_mat.csv"), 4)
    t_p1_get = gen_filenames("test1_{index}_out.csv", 4)
    t_p1_tim = gen_filenames("test1_{index}_out_time.csv", 4)

    # Problem 2A
    t_dir = os.path.join(test_dir, "Problem_2A")
    t_p2a_out = gen_filenames(os.path.join(t_dir, "test{index}_output_max.csv"), 4)
    t_p2a_get = gen_filenames("test2a_{index}_out.csv", 4)
    t_p2a_tim = gen_filenames("test2a_{index}_out_time.csv", 4)

    # Problem 2B
    t_dir = os.path.join(test_dir, "Problem_2B")
    t_p2b_out = gen_filenames(os.path.join(t_dir, "test{index}_output_second_max.csv"), 4)
    t_p2b_get = gen_filenames("test2b_{index}_out.csv", 4)
    t_p2b_tim = gen_filenames("test2b_{index}_out_time.csv", 4)

    # Problem 3
    t_dir = os.path.join(test_dir, "Problem_3")
    t_p3_in = gen_filenames(os.path.join(t_dir, "test{index}_text_input.txt"), 4)
    t_p3_out = gen_filenames(os.path.join(t_dir, "test{index}_text_output.txt"), 4)
    t_p3_get = gen_filenames("test3_{index}_out.csv", 8)
    t_p3_tim = gen_filenames("test3_{index}_out_time.csv", 8)

    # Problem 4
    t_dir = os.path.join(test_dir, "Problem_4")
    t_p4_in = gen_filenames(os.path.join(t_dir, "test{index}_text_to_decrypt_input.txt"), 1)
    t_p4_out = gen_filenames(os.path.join(t_dir, "test{index}_text_to_decrypt_output.txt"), 1)
    t_p4_get = gen_filenames("test4_{index}_out.csv", 4)
    t_p4_tim = gen_filenames("test4_{index}_out_time.csv", 4)

    # TA) TODO: for each problem, generate commands to make and run the test cases
    #   generate the commands to run the tests here
    c_p1  = []
    c_p2a = []
    c_p2b = []
    c_p3  = []
    c_p4  = []


    # TA) TODO: input matrix dimensions, if needed
    mat_dims = [[1000, 1000, 1000, 1000],
                [1000, 1000, 1000, 2000],
                [2000, 1000, 1000, 2000],
                [2000, 2000, 2000, 2000]]


    # TA) TODO: generate the problems' command-variables
    # problem 1, 2A, and 2B's command-variables
    for i in range(4):
        # Problem 1
        c_p1.append([
            "parallel_mult_mat_mat",
            t_mat_a[i], mat_dims[i][0], mat_dims[i][1],
            t_mat_b[i], mat_dims[i][2], mat_dims[i][3],
            16, t_p1_get[i], t_p1_tim[i]
        ])

        # Problem 2A
        c_p2a.append([
            "parallel_mult_max",
            t_mat_a[i], mat_dims[i][0], mat_dims[i][1],
            t_mat_b[i], mat_dims[i][2], mat_dims[i][3],
            16, t_p2a_get[i], t_p2a_tim[i]
        ])

        # Problem 2B
        c_p2b.append([
            "parallel_mult_second_largest",
            t_mat_a[i], mat_dims[i][0], mat_dims[i][1],
            t_mat_b[i], mat_dims[i][2], mat_dims[i][3],
            16, t_p2b_get[i], t_p2b_tim[i]
        ])

    # problem 3's command-variables
    for i in range(4):
        c_p3.append([
            "encrypt_parallel",
            10, t_p3_in[i], 16, t_p3_get[i], t_p3_tim[i]
        ])

    # problem 4's command-variables
    for i in range(1):
        c_p4.append([
            "decrypt_parallel",
            t_p4_in[i], 16, t_p4_get[i], t_p4_tim[i]
        ])

    #  we have everything we need to test a problem now
    #   grade each individual problem here!
    # TA) TODO: specify each problem's test parameters
    test_params = [
        [os.path.join(this_dir, "Problem_1"),  t_p1_out,  t_p1_get,  c_p1,  False],
        [os.path.join(this_dir, "Problem_2A"), t_p2a_out, t_p2a_get, c_p2a, False],
        [os.path.join(this_dir, "Problem_2B"), t_p2b_out, t_p2b_get, c_p2b, False],
        [os.path.join(this_dir, "Problem_3"),  t_p3_out,  t_p3_get,  c_p3,  True],
        [os.path.join(this_dir, "Problem_4"),  t_p4_out,  t_p4_get,  c_p4,  False]
    ]


    # testing results
    test_results = [None] * num_problems
    time_results = [None] * num_problems

    # test every problem in a loop
    grade_index = 0
    for i in range(num_problems):
        params = test_params[i]
        res = grade_problem(
            params[0],  # Problem dir
            params[1],  # Expected outputs of test i
            params[2],  # Output file names
            params[3],  # Command for getting test i results
            params[4]   # Whether to let the differences have an error range
        )

        # set results
        test_results[i] = res[0]
        time_results[i] = res[1]

        # add each result to the dataframes
        for p in range(len(params[3])):
            grade.loc[student_name, test_names[grade_index]] = test_results[i][p]
            try:
                time.loc[student_name, test_names[grade_index]] = time_results[i][p]
            except Exception as err:
                print(err)
            grade_index = grade_index + 1

    return [grade, time]

