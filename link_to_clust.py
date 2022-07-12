import numpy as np
import scipy.cluster.hierarchy as hierarchy
import scipy.spatial.distance as distance
import os

#loading the finished linkage array
processed = np.loadtxt(open('./script_data/fin', 'rb'),
                       delimiter=',',
                       skiprows=1)

#parse linkage array into clustering array
clusters = hierarchy.fcluster(processed, 100, criterion='maxclust')

#saving the clustering array
if not os.path.exists('script_data'):
    os.mkdir('script_data')
np.save('./script_data/clust', clusters)

print('clustering complete')
