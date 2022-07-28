# @author: broemere
# created: 7/21/2022
"""
~~~Description~~~
"""
from elib import *
import statsmodels.api as sm
from matplotlib.offsetbox import OffsetImage,AnchoredOffsetbox
import matplotlib.image as image
lowess = sm.nonparametric.lowess
runinit()
timer = runstartup()

samples = loadinterm("1-geometry")
g_TO_N = np.divide(9.807, 1000)
CAMERA_SCALE = 1/39

raw_images = rawdir / "raw_images"

plottype = "D"

plt.figure(dpi=150)
plt.title(plottype)

l0s = {}

for s in samples:

    if s._type == plottype:


        force = s.last_pull.force * g_TO_N
        stretch = np.array(s.heights) / s.heights[0]
        areas = []
        for a in s.areas:
            areas.append(np.mean(a)*CAMERA_SCALE*CAMERA_SCALE)
        stress = (force / np.array(areas)) * 1000  # kPa
        w = lowess(force, np.arange(0, len(force)), frac=0.4)
        force_lowess = w[:, 1]
        stress_lowess = (force_lowess / np.array(areas)) * 1000  # kPa

        w = lowess(stretch, np.arange(0, len(stretch)), frac=0.4)
        stretch_lowess = w[:, 1]

        l0 = round(s.heights[0] * CAMERA_SCALE, 1)
        l0s[s._label] = l0
        plt.scatter(stretch_lowess, stress_lowess, label=str(l0), marker=".")
        #axes[i].scatter(np.arange(0, len(stretch_lowess), w[:, 1], marker=".")
        plt.xlim(0.99, 1.21)
        plt.ylim(0, 250)


handles, labels = plt.gca().get_legend_handles_labels()
letterorder = sorted(l0s, key=l0s.get) # get list sorted by values
order = []
for l in letterorder:
    order.append(list(l0s.keys()).index(l))
plt.legend([handles[idx] for idx in order],[labels[idx] for idx in order])
plt.tight_layout()
plt.show()
plt.close()



