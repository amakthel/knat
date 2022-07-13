import matplotlib.pyplot as plt
import numpy as np

clusters = np.load('./script_data/clust.npy', allow_pickle=True)
feature_set = np.load('./script_data/reduced.npy')

fig, axs = plt.subplots(1, 3, figsize=[14.4, 4.8])

for n in range(np.shape(axs)[0]):
    axs[n].scatter(feature_set[:, n],
                    feature_set[:, (n+1)%3],
                    s=1,
                    c=clusters,
                    cmap='gist_rainbow')

plt.savefig('./plots/cluster_plots.png')
