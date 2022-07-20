import os
import subdivide_fcs

file_paths = [f for f in os.listdir('../samples') if os.path.isfile('../samples'+'/'+f)]

for file_path in file_paths:
    subdivide_fcs.cluster(file_path)
