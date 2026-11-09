#!/bin/bash
# Sample Slurm script for running ANSYS Fluent on TACC Stampede3.
# Runs the journal file run.jou in the directory you submit from.
# Submit with:  sbatch submit.slurm
#
# For your own case, change:
#   --job-name   any name you like
#   --ntasks     48 for a full skx node (96 with --nodes=2)
#   --time       long enough for your run (hh:mm:ss)
#   3ddp         use 2ddp for 2D cases
# Once your team has its own ACCESS allocation, uncomment the --account line
# and replace YOUR_PROJECT_ID with your team's project (e.g. TG-XXX000000).

#SBATCH --job-name=fluent_test
#SBATCH --partition=skx
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --time=00:10:00
#SBATCH --output=slurm-%j.out
#SBATCH --error=slurm-%j.err
##SBATCH --account=YOUR_PROJECT_ID

set -euo pipefail

module load ansys

cd "$SLURM_SUBMIT_DIR"

FLUENT=/home1/apps/ANSYS/2025R2/v252/fluent/bin/fluent

# List the compute nodes assigned to this job so Fluent knows where to run
scontrol show hostnames "$SLURM_JOB_NODELIST" > "hosts-${SLURM_JOB_ID}.txt"

"$FLUENT" 3ddp -g -t"${SLURM_NTASKS}" \
    -cnf="hosts-${SLURM_JOB_ID}.txt" \
    -scheduler_custom_script \
    -i run.jou > "fluent-${SLURM_JOB_ID}.log" 2>&1
