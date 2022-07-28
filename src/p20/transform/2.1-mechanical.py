# @author: broemere
# created: 7/18/2022
"""
~~~Description~~~
"""
from elib import *
import statsmodels.api as sm
lowess = sm.nonparametric.lowess
runinit()
timer = runstartup()

samples = loadinterm("1-geometry")
g_TO_N = np.divide(9.807, 1000)
CAMERA_SCALE = 1/39

for s in samples:
    if s.date != "2022-07-20":
        continue
    force = s.last_pull.force * g_TO_N
    stretch = np.array(s.heights) / s.heights[0]
    areas = []
    for a in s.areas:
        areas.append(np.mean(a)*CAMERA_SCALE*CAMERA_SCALE)
    stress = (force / np.array(areas)) * 1000  # kPa
    w = lowess(force, np.arange(0, len(force)), frac=0.4)
    force_lowess = w[:, 1]
    stress_lowess = (force_lowess / np.array(areas)) * 1000  # kPa


    plt.plot()
    #plt.scatter(np.arange(0, len(stretch)), stretch)
    plt.scatter(np.arange(0, len(s.data[s.last_i].force[s.start:s.stop])), s.data[s.last_i].force[s.start:s.stop])
    #plt.scatter(np.arange(0, len(w[:,1])), w[:,1], marker=".")
    #plt.scatter(stretch, force_lowess)
    plt.show()
    plt.close()


    break

    # break
    #
    #
    #
    #
    #     plt.plot()
    #     plt.scatter(np.arange(0, len(s.data[3].force)), s.data[3].force)
    #     plt.show()
    #     plt.close()