#!/bin/bash

#SBATCH --job-name=latte_bkg_sim
#SBATCH --output=logs/%A_%a.out
#SBATCH --error=logs/%A_%a.err
#SBATCH --time=01:30:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G

#SBATCH --array=1-10  # Creates 10 jobs, modify to do more/less

cd /path/to/project

pixi run remage  --gdml-files <gdml-file> --output-file sim_output/sim_run${SLURM_ARRAY_TASK_ID}.lh5 -- docs/macros/labbkgSim.mac 