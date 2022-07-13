from sklearn import cluster
from scipy.cluster import hierarchy
import numpy as np

try:
    feature_set = np.load('./script_data/reduced.npy',
                          allow_pickle=True)
except FileNotFoundError:
    print('there is no file at ./script_data/reduced.npy. have you '
        + 'run save_and_scale.py yet?')
except Exception:
    print('something unexpected has gone wrong while trying to load '
        + 'the feature set from ./script_data/reduced.npy. email '
        + 'iabenjamin@wpi.edu with this error.')
else:
    print('feature set loaded')

agglo = cluster.AgglomerativeClustering(n_clusters=4)
print('agglomerative clustering object created')

cluster_assignment = agglo.fit_predict(feature_set)
print('feature set analyzed')

np.save('./script_data/clust', cluster_assignment)
print('cluster assignment array saved')
