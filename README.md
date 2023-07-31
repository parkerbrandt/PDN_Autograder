# PDN Autograder
## Contributers: Paul Calle Contreras (2021), Jessica Shaw (2022), Parker Brandt (2023)

## What is it?

The PDN Autograder is a set of Python scripts designed to automatically run a student's code for each project, and then automatically test if that code correctly runs or not. It accomplishes this by running the student's code, and then checking the output via the provided test data folders to see if the student is correct or not.

There are individual autograders to run a single student's code for a single problem, then there are autograders that run a single student's code for every problem for a single project, then lastly, there are group autograders that will grade every students' submission for a single project. 


## How it Works

The autograder is structured such that there is a singular "base autograder" that holds the code that every project problem will need to use to grade and compare each problem.


## How to Run

### File Structure


### Using Schooner

There are provided SBATCH files that can run the autograder code on the Schooner supercomputer. Note that the SBATCH files must be edited to the right email and user names to run correctly. 


NOTE: Having a separate partition from oucspdn_cpu may be helpful as the 15 minute time limit may not be enough


## How to Create More Tests

With the updates to the autograder, it should be straight-forward on how to create more tests for future problems. As can be seen, there is a structure to each autograder that can be followed with minor adjustments to account for filepaths and arguments. 

Once a new class is created for this autograder problem, that class must have 3 methods:

- __init__() : to initialize the object's variables. It must be noted that the __init__() method in all current autograders uses a series of parameters that allow the group autograders to change where the directories are located.

- is_error_within_bound() : to check how correct the problem 

- autograde() : to set up the necessary file paths to each problem's code and test data, set up the commands needed to run the code, and then to send that information to the base autograder


## How to Write a Group Autograder

Creating a group autograder is also simple by following the structure created in the other group autograders provided. If the individual autograders are already written, the group autograder will mostly be calling those individual autograders to run student code with some set up. The set up a group autograder must do is:

- Unzip all student submissions (if not already unzipped")

- Flatten the directories in case students have nested directories

- Grade each student submission 

- Output all results to a CSV file


### Improvements to be Made

- Allow time files to be more than just 1 value, and if they contain more than that, sum up the values
- Allow file structure to be more loose or easier to understand/account for more student error


### Contact

If you have any questions or concerns, feel free to email me at pbrandt@ou.edu or parker.brandt101@gmail.com for more information.