import os
import subdivide_fcs

folders = ['beads', 'samples']

for folder in folders:
    names = [f for f in os.listdir('../'+folder) if os.path.isfile('../'+folder+'/'+f)]
    for name in names:
        subdivide_fcs.cluster(folder, name)
