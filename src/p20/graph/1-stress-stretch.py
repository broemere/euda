# @author: broemere
# created: 7/28/2022
"""
~~~Description~~~
"""
from elib import *
runinit()
timer = runstartup()

samples = loadinterm("2-mech")
g_TO_N = np.divide(9.807, 1000)
CAMERA_SCALE = 1 / 39
cmap = cm.get_cmap("cool", 10)
colors = cmap(np.arange(0, cmap.N))

drop = ["07D", "31C", "31D", "34C", "34D", "36C", "36D"]

plt.figure(dpi=150)
for s in samples:
    if s._label in drop or s._type == "D":
        continue
    if s.sex == "M":
        plt.scatter(s.stretch_lowess, s.stress, marker=".", color="blue", label="Male")
    if s.sex == "F":
        plt.scatter(s.stretch_lowess, s.stress, marker=".", color=colors[-1], label="Female")
plt.legend(*[*zip(*{l: h for h, l in zip(*plt.gca().get_legend_handles_labels())}.items())][::-1])
plt.xlabel("Stretch")
plt.ylabel("Stress [kPa]")
plt.title("With Cells")
plt.xlim(.99, 1.25)
plt.ylim(0, 250)
plt.show()
plt.close()

plt.figure(dpi=150)
for s in samples:
    if s._label in drop or s._type == "C":
        continue
    if s.sex == "M":
        plt.scatter(s.stretch_lowess, s.stress, marker=".", color="blue", label="Male", alpha=0.25)
    if s.sex == "F":
        plt.scatter(s.stretch_lowess, s.stress, marker=".", color=colors[-1], label="Female", alpha=0.25)
plt.legend(*[*zip(*{l: h for h, l in zip(*plt.gca().get_legend_handles_labels())}.items())][::-1])
plt.xlabel("Stretch")
plt.ylabel("Stress [kPa]")
plt.title("Decelled")
plt.xlim(.99, 1.25)
plt.ylim(0, 250)
plt.show()
plt.close()

