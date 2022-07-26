#!/usr/bin/env bash

#SBATCH -N1 --mem-per-cpu=256G

python process_samples.py
