# @author: broemere
# created: 7/29/2022
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

drop = []

for s in samples:
    s.volumes_one_gram = []
    for v in s.voxel_one_gram:
        vol = np.sum(v)*(CAMERA_SCALE**3)
        s.volumes_one_gram.append(vol)

plt.figure(dpi=150)
for s in samples:

    if s._label in drop or s._type == "D":
        continue
    for i in range(s.last_i+1):
        if s.sex == "M":
            plt.scatter(i+np.random.randint(-10, 10)/100, s.volumes_one_gram[i], color="blue", label="Male")
        if s.sex == "F":
            plt.scatter(i+5+np.random.randint(-10, 10)/100, s.volumes_one_gram[i], color=colors[-1], label="Female")

plt.legend(*[*zip(*{l: h for h, l in zip(*plt.gca().get_legend_handles_labels())}.items())][::-1])
#plt.xlabel("Stretch")
plt.ylabel("Volume [mm3]")
plt.title("With Cells")
#plt.xlim(-.99, 1.99)
plt.ylim(3, 40)
plt.gca().set_xticks([0,1,2,3, 5,6,7,8,9,10], ["10%","20%","30%","40%", "10%","20%","30%","40%","50%","60%"])
plt.show()
plt.close()


plt.figure(dpi=150)
for s in samples:
    if s._label in drop or s._type == "C":
        continue
    for i in range(s.last_i+1):
        if s.sex == "M":
            plt.scatter(i+np.random.randint(-10, 10)/100, s.volumes_one_gram[i], color="blue", label="Male", alpha=0.25)
        if s.sex == "F":
            plt.scatter(i+5+np.random.randint(-10, 10)/100, s.volumes_one_gram[i], color=colors[-1], label="Female", alpha=0.25)
            #facecolor="none"

plt.legend(*[*zip(*{l: h for h, l in zip(*plt.gca().get_legend_handles_labels())}.items())][::-1])
#plt.xlabel("Stretch")
plt.ylabel("Volume [mm3]")
plt.title("Decelled")
#plt.xlim(-.99, 1.99)
plt.ylim(3, 40)
plt.gca().set_xticks([0,1,2,3, 5,6,7,8,9,10], ["10%","20%","30%","40%", "10%","20%","30%","40%","50%","60%"])
plt.show()
plt.close()