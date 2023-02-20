from autograder_problem_3_2 import Autograder_3_2
from autograder_problem_3_3 import Autograder_3_3
from autograder_problem_3_4 import Autograder_3_4
from termcolor import colored


# 
def main():
    print(colored("Autograding for Project 3:\n", "green"))

    # Grade Problem 2
    print(colored("Autograding for Project 3 Problem 2:\n", "green"))
    p2 = Autograder_3_2()
    res2 = p2.autograde()
    total2 = str(len(res2[0].columns))
    correct2 = str(int(res2[0].sum(axis=1)[0]))

    # Grade Problem 3
    print(colored("Autograding for Project 3 Problem 3:\n", "green"))
    p3 = Autograder_3_3()
    res3 = p3.autograde()
    total3 = str(len(res3[0].columns))
    correct3 = str(int(res3[0].sum(axis=1)[0]))

    # Grade Problem 4
    print(colored("Autograding for Project 3 Problem 4:\n", "green"))
    p4 = Autograder_3_4()
    res4 = p4.autograde()
    total4 = str(len(res4[0].columns))
    correct4 = str(int(res4[0].sum(axis=1)[0]))
  
    # Print results
    print(colored("\n Problem 2 Final Grades:", "yellow"))
    print(res2[0])

    print(colored("\n Problem 3 Final Grades:", "yellow"))
    print(res3[0])

    print(colored("\n Problem 4 Final Grades:", "yellow"))
    print(res4[0])

    correct = correct2 + correct3 + correct4
    total = total2 + total3 + total4 
    print(colored(f"\n --> {correct}/{total} problems correct\n", "red"))

    return


if __name__ == "__main__":
    main()