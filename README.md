# knat

attempting to use machine learning do identify useful sub-populations
in flow cytometry data on K. nataicola bacteria.

Currently the code is constructed as a bash script that runs a python
script which imports the function that actually does the machine
learning from subdivide_fcs and applies it to all the relevant data.
link_to_clust.py, save_and_scale.py, agglom.py, and plot_clust.py are
depreciated now that we use scikit-learn and check a variety of numbers
of clusters. subdivide_fcs.py provides a subdivide() function that takes
a particular sample given a directory and sample name, pulls flow
cytometry data from it, transforms it to rfi, scales it down with sinh
scaling, trims off less important channels, creates an
AgglomerativeClustering object to handle the new feature set, and fits
that object to the data. It produces a numpy array of the clusters to
which each observation is assigned, and plots the data in numerous ways
based on the different channels in the original data, highlighting the
clusters with the dark2 color palette. process_samples.py creates an
array of file names for each directory of samples, and runs through all
of the samples in the chosen directories (currently beads/ and samples/
in the parent directory of the repository). slurm_compatible.sh is a
bash script whose only purpose is to provide parameters to sbatch and
run process_samples.py.
