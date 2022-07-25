import os
from subdivide_fcs import subdivide

folders = ['beads', 'samples']

for folder in folders:
    names = [f for f in os.listdir('../'+folder) if os.path.isfile('../'+folder+'/'+f)]
    for name in names:
        subdivide(folder, name)
