from sklearn import cluster
from scipy.cluster import hierarchy
import numpy as np

feature_set = np.load('./script_data/reduced.npy', allow_pickle=True)
print('feature set loaded')

agglo = cluster.AgglomerativeClustering(n_clusters=4)
print('agglomerative clustering object created')

cluster_assignment = agglo.fit_predict(feature_set)
print('feature set analyzed')

np.save('./script_data/clust', cluster_assignment)
print('made it this far!')

