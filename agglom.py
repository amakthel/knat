from sklearn import cluster
from scipy.cluster import hierarchy
import numpy as np

feature_set = np.load('./script_data/reduced.npy')
print('feature set loaded')

agglo = cluster.AgglomerativeClustering(n_clusters=8)
print('agglomerative clustering object created')

cluster_assignment = agglo.fit(feature_set)
print('feature set analyzed')
np.save('./script_data/clust', cluster_assignment)
print('made it this far!')

