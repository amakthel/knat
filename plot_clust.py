import matplotlib.pyplot as plt
import numpy as np

clusters = np.load('./script_data/clust.npy', allow_pickle=True)
feature_set = np.load('./script_data/reduced.npy')

fig, axes = plt.subplots(1, 3)

for n in range(np.shape(axes)[0]):
    axes[n].scatter(feature_set[:, n],
                    feature_set[:, (n+1)%3],
                    s=1,
                    c=clusters,
                    cmap='gist_rainbow')

plt.savefig('./plots/cluster_plots.png')
