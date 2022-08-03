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

    s.force = (s.last_pull.force - np.mean(s.last_pull.force.iloc[0:10])) * g_TO_N
    s.stretch = np.array(s.heights) / s.heights[0]

    area_mean = np.mean(np.sum(np.sum(s.voxel_first, axis=1), axis=0))
    w_means = []
    for img in s.th_imgs:
        w_means.append(np.mean(np.sum(img_hardcrop(img), axis=1)))

    t_initial = np.mean(np.sum(s.side_one_gram[s.last_i], axis=1))

    wt = []
    tt = []
    for i, lam in enumerate(s.stretch):
        wt.append(w_means[i])

    wt_stretch = np.array(wt) / wt[0]

    for i, lam in enumerate(s.stretch):
        tt.append((t_initial * np.sqrt(np.divide(1, lam*wt_stretch[i]))))

    areas = np.array(wt) * tt
    s.areas = areas * (CAMERA_SCALE**2)
    force_lowess = get_lowess(s.force)

    s.stretch_lowess = get_lowess(s.stretch)
    s.stress = (force_lowess / s.areas) * 1000

    s.stress_range = np.arange(math.ceil(s.stress[0]), math.floor(s.stress[-1]))
    s.stretch_interp = []
    for i, v in enumerate(s.stress_range):
        nearest_stress_i = np.abs(s.stress - v).argmin()
        stretch_avg = np.mean(s.stretch_lowess[nearest_stress_i - 1:nearest_stress_i + 2])
        s.stretch_interp.append(stretch_avg)


writeinterm("2-mech", samples)

