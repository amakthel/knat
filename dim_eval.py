import FlowCal
import statistics as st
import numpy as np

bead_file_name = 'beads-1.fcs'
bead_path = '../beads/'+bead_file_name
pre_reduction_path = './script_data/pre-reduction.npy'
post_reduction_path = './script_data/post-reduction.npy'

try:
    beads = FlowCal.io.FCSData(bead_path)
except FileNotFoundError:
    print('there is no file at '
        + bead_path
        + ' . make sure that you have the correct path.')
except Exception:
    print('something unexpected went wrong while trying to process the'
        + ' .fcs file. email iabenjamin@wpi.edu with this error.')
else:
    print('flow cytometry data successfully drawn from bead file.')

try:
    pre = np.load(pre_reduction_path, allow_pickle=True)
except FileNotFoundError:
    print(pre_reduction_path
        + ' is not present. have you run subdivide_fcs.py yet?')
except Exception:
    print('something unexpected went wrong while trying to load the '
        + 'pre-dimensional analysis flow cytometry data. email '
        + 'iabenjamin@wpi.edu with this error.')
else:
    print('pre-dimensional analysis flow cytometry data successfully '
        + 'loaded.')

try:
    post = np.load(post_reduction_path, allow_pickle=True)
except FileNotFoundError:
    print(post_reduction_path
        + ' is not present. have you run subdivide_fcs.py yet?')
except Exception:
    print('something unexpected went wrong while trying to load the '
        + 'post-dimensional analysis flow cytometry data. email '
        + 'iabenjamin@wpi.edu with this error.')
else:
    print('post-dimensional analysis flow cytometry data successfully '
        + 'loaded.')

channel_names = beads.channels
vari_path = './script_data/variances'
corr_path = './script_data/correlation_coefficients'
number_of_channels = np.shape(beads)[1]

variances = np.zeros(number_of_channels)
for i in range(number_of_channels):
    variances[i] = st.variance(pre[:, i])

corr_coeffs = np.corrcoef(pre, rowvar=False)

np.save(vari_path, variances)
np.save(corr_path, corr_coeffs)

