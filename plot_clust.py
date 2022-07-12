import matplotlib.pyplot as plt
import numpy as np

clusters = np.load('./script_data/clust.npy', allow_pickle=True)
feature_set = np.load('./script_data/reduced.npy')

fig, axes = plt.subplots(1, 3)

axes[0].scatter(feature_set[:, 0], feature_set[:, 1], s=20, c=clusters, cmap='gist_rainbow')
axes[0].set_xlabel('FSC-A')
axes[0].set_ylabel('SSC-A')

axes[1].scatter(feature_set[:, 1], feature_set[:, 2], s=20, c=clusters, cmap='gist_rainbow')
axes[1].set_xlabel('SSC-A')
axes[1].set_ylabel('FL1-A')

axes[2].scatter(feature_set[:, 2], feature_set[:, 0], s=20, c=clusters, cmap='gist_rainbow')
axes[2].set_xlabel('FL1-A')
axes[2].set_ylabel('FSC-A')

plt.savefig('./plots/cluster_plots.png')
