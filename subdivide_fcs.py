import FlowCal
import os
import numpy as np
import statistics as st
import matplotlib.pyplot as plt
from sklearn import preprocessing as prep
from sklearn import decomposition as decomp
from sklearn import cluster
from scipy.cluster import hierarchy


def sinhScaling(x):
    return np.arcsinh(x)/np.log(10)

def subdivide(dir_path, path_input):
    file_name = path_input[:-4]
    file_path = '../'+dir_path+'/'+path_input

    try:
        flow_data = FlowCal.io.FCSData(file_path)
    except FileNotFoundError:
        print('there is no file at '
            + file_path
            + ' . make sure that you have the correct path')
    except Exception:
        print('something unexpected went wrong while trying to process the'
              ' .fcs file. email iabenjamin@wpi.edu with this error.')
    else:
        print('flow cytometry data successfully drawn from bead file')

    # Removes first 250 and last 100 events,
    # used in FlowCal excel_ui script
    flow_data = FlowCal.gate.start_end(flow_data, num_start=250, num_end=100)
    # this converts the raw voltage values for FL1-A (GFP-A) to
    # Relative Fluorescent Intensity (AU)
    transformed_data = FlowCal.transform.to_rfi(flow_data, channels='FL1-A')
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
    scaled_data = FlowCal.transform.transform(transformed_data,
                                           channels=None,
                                           transform_fxn=sinhScaling)
    scaled_data = FlowCal.transform.transform(scaled_data,
                                           channels=None,
                                           transform_fxn=lambda x: x/8)
    print('flow cytometry data successfully scaled')
    if not os.path.exists('./script_data'):
        os.mkdir('script_data')
    if not os.path.exists('./script_data/'+dir_path):
        os.mkdir('script_data/'+dir_path)
    if not os.path.exists('./script_data/'+dir_path+'/'+file_name):
        os.mkdir('script_data/'+dir_path+'/'+file_name)
    np.save('./script_data/'+dir_path+'/'+file_name+'/pre-reduction', scaled_data)

    channel_names = scaled_data.channels
    vari_path = './script_data/'+dir_path+'/'+file_name+'/variances'
    covs_path = './script_data/'+dir_path+'/'+file_name+'/covariances'
    number_of_channels = np.shape(scaled_data)[1]

    variances = np.zeros(number_of_channels)
    for i in range(number_of_channels):
        variances[i] = st.variance(scaled_data[:, i])
    np.save(vari_path, variances)
    def invalid(n):
        return variances[n] < 0.01
    kept_channels = [
            channel_names[i]
            for i 
            in range(number_of_channels) 
            if not invalid(i)
            ]
    trimmed_data = scaled_data[:, kept_channels]
    covars = np.cov(trimmed_data, rowvar=False)
    np.save(covs_path, covars)

    scaler = prep.StandardScaler()
    pca2 = decomp.PCA(n_components=2)
    centered_data = scaler.fit_transform(trimmed_data)
    feature_set = pca2.fit_transform(centered_data)

    np.save('./script_data/'+dir_path+'/'+file_name+'/post-reduction', feature_set)

    print('excess features successfully trimmed from the flow cytometry data')

    for cluster_number in range(3, 16):
        agglo = cluster.AgglomerativeClustering(n_clusters=cluster_number)
        print('agglomerative clustering object ({:n} clusters) created'\
                .format(cluster_number))
        cluster_assignment = agglo.fit_predict(feature_set)
        print('feature set analyzed into {:n} clusters'\
                .format(cluster_number))
        fig, axs = plt.subplots(1, 3, figsize=[14.4, 4.8])

        axs[0].scatter(trimmed_data[:, ['FSC-A']],
                       trimmed_data[:, ['SSC-A']],
                       s=0.1,
                       c=cluster_assignment,
                       cmap='gist_rainbow')
        axs[1].scatter(trimmed_data[:, ['SSC-A']],
                       trimmed_data[:, ['FL1-A']],
                       s=0.1,
                       c=cluster_assignment,
                       cmap='gist_rainbow')
        axs[2].scatter(trimmed_data[:, ['FL1-A']],
                       trimmed_data[:, ['FSC-A']],
                       s=0.1,
                       c=cluster_assignment,
                       cmap='gist_rainbow')
        axs[0].set_xlabel('FSC-A')
        axs[0].set_ylabel('SSC-A')
        axs[1].set_xlabel('SSC-A')
        axs[1].set_ylabel('FL1-A')
        axs[2].set_xlabel('FL1-A')
        axs[2].set_ylabel('FSC-A')
        if not os.path.exists('./plots/'):
            os.mkdir('plots')
        if not os.path.exists('./plots/'+dir_path):
            os.mkdir('./plots/'+dir_path)
        if not os.path.exists('./plots/'+dir_path+'/'+file_name):
            os.mkdir('plots/'+file_name)
        plt.savefig('./plots/'+dir_path+'/'+file_name+'/cluster_plots{:n}.png'.format(cluster_number))
