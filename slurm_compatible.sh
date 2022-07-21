#!/usr/bin/env bash

#SBATCH -N1 -n1 --mem-per-cpu=128G -t00:20:00

exec python process_samples.py

exit $?
