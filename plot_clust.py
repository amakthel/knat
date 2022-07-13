import matplotlib.pyplot as plt
import numpy as np

try:
    clusters = np.load('./script_data/clust.npy', allow_pickle=True)
except FileNotFoundError:
    print('there is no file at ./script_data/clust.npy, have you run
           agglom.py yet?')
except Exception:
    print('something unexpected went wrong while loading
           ./script_data/clust.npy. email iabenjamin@wpi.edu with this
           error.')

try:
    feature_set = np.load('./script_data/reduced.npy')
except FileNotFoundError:
    print('there is no file at ./script_data/reduced.npy. have you run
           save_and_scale.py yet?')
except Exception:
    print('something unexpected went wrong while loading
           ./script_data/reduced.npy. email iabenjamin@wpi.edu with
           this error.')

fig, axs = plt.subplots(1, 3, figsize=[14.4, 4.8])

for n in range(np.shape(axs)[0]):
    axs[n].scatter(feature_set[:, n],
                    feature_set[:, (n+1)%3],
                    s=1,
                    c=clusters,
                    cmap='gist_rainbow')

plt.savefig('./plots/cluster_plots.png')
