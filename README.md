# PDN Autograder
## Contributers: Paul Calle Contreras (2021), Jessica Shaw (2022), Parker Brandt (2023)

## What is it?

The PDN Autograder is a set of Python scripts designed to automatically run a student's code for each project, and then automatically test if that code correctly runs or not. It accomplishes this by running the student's code, and then checking the output via the provided test data folders to see if the student is correct or not.

There are individual autograders to run a single student's code for a single problem, then there are autograders that run a single student's code for every problem for a single project, then lastly, there are group autograders that will grade every students' submission for a single project. 


## How it Works

The autograder is structured such that there is a singular "base autograder" that holds the code that every project problem will need to use to grade and compare each problem.

Each individual autograder then inherits from that base autograder class and then overrides the necessary methods, and implements its own logic. The most complicated logic comes from the base autograder performing the actual autograding, so by abstracting each individual autograder away, it allows for less error. 

Each group autograder and project autograder then calls the individual autograders to perform the logic again.


## How to Run

### File Structure


### Using Schooner

There are provided SBATCH files that can run the autograder code on the Schooner supercomputer. Note that the SBATCH files must be edited to the right email and user names to run correctly. 


NOTE: Having a separate partition from oucspdn_cpu may be helpful as the 15 minute time limit may not be enough


## How to Create More Tests

With the updates to the autograder, it should be straight-forward on how to create more tests for future problems. As can be seen, there is a structure to each autograder that can be followed with minor adjustments to account for filepaths and arguments. 

Once a new class is created for this autograder problem, that class must have 3 methods:

- __init__() : to initialize the object's variables. It must be noted that the __init__() method in all current autograders uses a series of parameters that allow the group autograders to change where the directories are located. Some important variables that are initialized in __init__() include:
    - student_name : the string name of the student being graded
    - is_grad : the boolean telling if the student is a graduate student or not (NOTE: this is not used as of right now and is automatically set to true, but may be a good improvement in the future)
    - DEBUG : tells the script whether to output debug statements or not (automatically set to true)
    - this_dir : the directory in which the autograding script resides
    - student_files : the directory in which the student's code and files reside
    - test_files : the directory in which the test data files reside
    - threads : the set of integer threads to test with, will perform each test with each number of threads provided in array
    - test_names : the names of the tests that will be performed

- is_error_within_bound() : to check how correct the problem is by comparing the student's code to the test data code. Allows for each problem to have its own individual way of checking how correct a problem needs to be.

- autograde() : to set up the necessary file paths to each problem's code and test data, set up the commands needed to run the code, and then to send that information to the base autograder. This function will then return the array of grades and times that it receives back from the base autograder


## How to Write a Group Autograder

Creating a group autograder is also simple by following the structure created in the other group autograders provided. If the individual autograders are already written, the group autograder will mostly be calling those individual autograders to run student code with some set up. The set up a group autograder must do is:

- Unzip all student submissions (if not already unzipped")

- Flatten the directories in case students have nested directories

- Grade each student submission by calling the individual autograders, and then providing them the necessary file paths and information through parameters when creating the objects

- Output all results to a CSV file

NOTE: The file structure for the group autograder will be slightly different. There will not be a individual autograder in each student's folder, but rather the individual autograder will reside on the same level as the group autograder. 


## Other Resources

I will be recording myself running each of the autograders, and those recording should be made available as an example for running each one, and can be used to see how the file structure is set up.


## Improvements to be Made

- Allow time files to be more than just 1 value, and if they contain more than that, sum up the values
- Allow file structure to be more loose or easier to understand/account for more student error


## Contact

If you have any questions or concerns, feel free to email me at pbrandt@ou.edu or parker.brandt101@gmail.com for more information.