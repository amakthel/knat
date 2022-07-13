import FlowCal
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn import cluster
from scipy.cluster import hierarchy

bead_file_name = 'beads-1.fcs'
bead_path = '../beads/'+bead_file_name

try:
    b = FlowCal.io.FCSData(bead_path)
except FileNotFoundError:
    print('there is no file at '
        + bead_path
        + ' . make sure that you have the correct path')
except Exception:
    print('something unexpected went wrong while trying to process the'
          ' .fcs file. email iabenjamin@wpi.edu with this error.')
else:
    print('flow cytometry data successfully drawn from bead file')

# Removes first 250 and last 100 events,
# used in FlowCal excel_ui script
b = FlowCal.gate.start_end(b, num_start=250, num_end=100)
# this converts the raw voltage values for FL1-A (GFP-A) to
# Relative Fluorescent Intensity (AU)
b_transformed = FlowCal.transform.to_rfi(b, channels='FL1-A')
print('flow cytometry data successfully transformed to Relative '
      'Fluorescent Intensity')

# FSCData type arrays have additional features compared to numpy arrays.
# A non-exhaustive list:
# names for the various columns associated with a
# particular channel on the flow cytometer
# a hidden range variable for each column that keeps track of the
# interval occupied by the data in that column
#
# Because of the second of the above two features, when scaling a
# FSCData array, you need to use FlowCal.transform.transform so that the
# range is scaled along with the array data. In general try to use
# FlowCal methods and functions on FSCData objects because functions
# meant for numpy arrays can occasionally remove the channel and range
# data.
def sinhScaling(x):
    return np.arcsinh(x)/np.log(10)
b_scaled = FlowCal.transform.transform(b_transformed,
                                       channels=None,
                                       transform_fxn=sinhScaling)
b_scaled = FlowCal.transform.transform(b_scaled,
                                       channels=None,
                                       transform_fxn=lambda x: x/8)
print('flow cytometry data successfully scaled')
# all other features of the data set are either enormously correlated
# or very low variance and are  therefore not needed for the analysis
feature_set = b_scaled[:, ['FSC-A', 'SSC-A', 'FL1-A']]
print('features successfully trimmed from the flow cytometry data')
for cluster_number in range(3, 16):
    agglo = cluster.AgglomerativeClustering(n_clusters=cluster_number)
    print('agglomerative clustering object ({:n} clusters) created'\
            .format(cluster_number))
    with agglo.fit_predict(feature_set) as cluster_assignment:
        print('feature set analyzed into {:n} clusters'\
                .format(cluster_number))
        fig, axs = plt.subplots(1, 3, figsize=[14.4, 4.8])
        for n in range(np.shape(axs)[0]):
            axs[n].scatter(feature_set[:, n],
                            feature_set[:, (n+1)%3],
                            s=1,
                            c=cluster_assignment,
                            cmap='gist_rainbow')
        axs[0].set_xlabel('FSC-A')
        axs[0].set_ylabel('SSC-A')
        axs[1].set_xlabel('SSC-A')
        axs[1].set_ylabel('FL1-A')
        axs[2].set_xlabel('FL1-A')
        axs[2].set_ylabel('FSC-A')
        plt.savefig('./plots/cluster_plots{:n}.png'.format(number_of_clusters))
