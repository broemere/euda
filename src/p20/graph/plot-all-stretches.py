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

def place_image(im, loc=3, ax=None, zoom=1, **kw):
    if ax==None: ax=plt.gca()
    imagebox = OffsetImage(im, zoom=zoom*0.12)
    ab = AnchoredOffsetbox(loc=loc, child=imagebox, frameon=False, **kw)
    ax.add_artist(ab)


for d in os.listdir(raw_images):
    fig, axes = plt.subplots(1, 3, figsize=(12,3.5))
    fig.suptitle(d.replace("_","/"))
    i = 0

    for s in samples:
        if s.date == d.replace("_","-"):

            im = cv2.cvtColor(s.th_imgs[0]*255, cv2.COLOR_GRAY2RGB)

            force = s.last_pull.force * g_TO_N
            stretch = np.array(s.heights) / s.heights[0]
            areas = []
            for a in s.areas:
                areas.append(np.mean(a)*CAMERA_SCALE*CAMERA_SCALE)
            stress = (force / np.array(areas)) * 1000  # kPa
            w = lowess(force, np.arange(0, len(force)), frac=0.4)
            force_lowess = w[:, 1]
            stress_lowess = (force_lowess / np.array(areas)) * 1000  # kPa

            axes[i].scatter(np.arange(0, len(stretch)), stretch)
            #axes[i].scatter(np.arange(0, len(stretch_lowess), w[:, 1], marker=".")
            axes[i].set_ylim(0.97, 1.21)
            if i > 0:
                axes[i].set_yticks([])

            l0 = round(s.heights[0] * CAMERA_SCALE, 1)

            #axes[i].text(20, 0.15, f"{l0}")
            axes[i].set_title(s._type)

            place_image(im, loc=2, ax=axes[i], pad=0, zoom=1)

            i += 1

    axes[2].set_yticks([])

    plt.tight_layout()
    plt.show()
    plt.close()


