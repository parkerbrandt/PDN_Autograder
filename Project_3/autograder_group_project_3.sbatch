#!/bin/bash
#
#SBATCH --partition=oucspdn_cpu
#
#SBATCH --ntasks=8
#SBATCH --ntasks-per-node=8
#
#SBATCH --job-name=auto_P3
#
#
#SBATCH --mail-user=pbrandt@ou.edu
#SBATCH --mail-type=ALL
#
#SBATCH --chdir=/home/oucspdnta/ta_only/Autograding/Project_3/
#SBATCH --output=/home/oucspdnta/ta_only/Autograding/Project_3/output/autograding_%J_stdout.txt
#SBATCH --error=/home/oucspdnta/ta_only/Autograding/Project_3/output/autograding_%J_stderr.txt

#################################################

module purge

module load SciPy-bundle/2020.03-foss-2020a-Python-3.8.2

python3 -u autograder_group_project_3.py