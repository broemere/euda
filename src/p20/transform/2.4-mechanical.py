# @author: broemere
# created: 7/18/2022
"""
~~~Description~~~
"""
from elib import *
runinit()
timer = runstartup()

samples = loadinterm("2-voxels")
g_TO_N = np.divide(9.807, 1000)
CAMERA_SCALE = 1/39

for s in samples:

    s.force = s.last_pull.force * g_TO_N
    s.stretch = np.array(s.heights) / s.heights[0]

    area_mean = np.mean(np.sum(np.sum(s.voxel_first, axis=1), axis=0))
    w_means = []
    for img in s.th_imgs:
        w_means.append(np.mean(np.sum(img_hardcrop(img), axis=1)))

    wt = []
    tt = []
    for i, lam in enumerate(s.stretch):
        wt.append(w_means[i] * np.sqrt(np.divide(1, lam)))
        tt.append((area_mean/w_means[i]) * np.sqrt(np.divide(1, lam)))

    areas = np.array(wt) * tt
    s.areas = areas * (CAMERA_SCALE**2)
    force_lowess = get_lowess(s.force)

    s.stretch_lowess = get_lowess(s.stretch)
    s.stress = (force_lowess / s.areas) * 1000


writeinterm("2-mech", samples)

