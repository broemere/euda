# @author: broemere
# created: 7/28/2022
"""
Description
"""
from elib import *
from mayavi import mlab
runinit()

samples = loadinterm("2-voxels")

s = samples[0]

mlab.figure(1, fgcolor=(0, 0, 0), bgcolor=(1, 1, 1), size=(1080, 1080))
coords = s.voxel_first.nonzero()
mlab.points3d(coords[0], coords[1], coords[2], mode="cube", color=(0.25, 0.25, 1), scale_factor=1)
mlab.orientation_axes()
#mlab.view(azimuth=-10 - (i * 7.2), elevation=70)
#num = str(s.last_i+1) + "%"
#filename = f"{s._label}_{num}.png"
#filepath = vizdir / filename
#mlab.savefig(str(filepath), magnification=3)
mlab.show()
#mlab.clf()
#mlab.close()