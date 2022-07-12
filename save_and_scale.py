import FlowCal
import numpy as np
import os
import scipy

# change below as needed
bead_file_name = 'beads-1.fcs'

#you should not need to change the below code
bead_path = '../beads/'+bead_file_name
b = FlowCal.io.FCSData(bead_path)

print('flow cytometry data successfully drawn from bead file')

# Removes first 250 and last 100 events, used in FlowCal excel_ui script
b = FlowCal.gate.start_end(b, num_start=250, num_end=100)
# this converts the raw voltage values for FL1-A (GFP-A) to Relative
# Fluorescent Intensity (AU)
b_transformed = FlowCal.transform.to_rfi(b, channels='FL1-A')

print('flow cytometry data successfully transformed to rfi')

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
if not os.path.exists('script_data'):
    os.mkdir('script_data')
np.savetxt('./script_data/reduced.csv', feature_set, delimiter=",")
np.save('./script_data/reduced', feature_set)

print('feature set successfully trimmed from flow cytometry data: ')
print(feature_set)
