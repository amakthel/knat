#!/usr/bin/env bash

#SBATCH -N1 -n1 --mem-per-cpu=128G -t00:30:00

python process_samples.py
