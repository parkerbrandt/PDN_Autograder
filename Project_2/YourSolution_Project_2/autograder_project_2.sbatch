#!/bin/bash
# Choose the partition that you will use.
# You can choose: oucspdn_cpu OR debug_5min OR debug OR others 
#
#SBATCH --partition=oucspdn_cpu
#
#SBATCH --ntasks=8
#SBATCH --ntasks-per-node=8
#
#SBATCH --time=00:15:00
#SBATCH --job-name=auto
#
#
# --------------------- Change the items below here! ---------------------
#
#SBATCH --mail-user=youremail@ou.edu
#SBATCH --mail-type=ALL
#
#SBATCH --chdir=/home/user007/HW2/
#SBATCH --output=/home/user007/HW2/autograding_%J_stdout.txt
#SBATCH --error=/home/user007/HW2/autograding_%J_stderr.txt

#################################################

module purge

module load SciPy-bundle/2020.03-foss-2020a-Python-3.8.2

# To run all the problems and get all results
python3 -u autograder_project_2.py

# To run just problem 1's autograder
# python3 -u autograder_problem_2_1.py

# To run just problem 2's autograder
# python3 -u autograder_problem_2_2.py

# To run just problem 3's autograder
# python3 -u autograder_problem_2_3.py

# To run just problem 4's autograder
# python3 -u autograder_problem_2_4.py