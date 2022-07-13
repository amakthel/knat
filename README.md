# knat

attempting to use machine learning do identify useful sub-populations
in flow cytometry data on K. nataicola bacteria.

Currently the code is constructed as a single script: link_to_clust.py,
save_and_scale.py, agglom.py, and plot_clust.py are depreciated now
that we use scikit-learn and check a variety of numbers of clusters.
subdivide_fcs.py pulls flow cytometry data from an .fcs file, transforms
it to rfi, scales it down with sinh scaling, trims off less important
channels, creates an AgglomerativeClustering object to handle the new
feature set, and fits that object to the data. It produces a numpy array
of the clusters to which each observation is assigned, and plots the
data, highlighting the clusters with the dark2 color palette.
