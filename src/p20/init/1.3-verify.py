# @author: broemere
# created: 7/27/2022
"""
Show sample metadata and data trim plots
"""
from elib import *
runinit()
timer = runstartup()

samples = loadinterm("1-live-imgs")

males = 0
females = 0

cmap = cm.get_cmap("cool", 6)
colors = cmap(np.arange(0, cmap.N))
# colors = colors[::-1]
fhdir = vizdir / "force-height"
mkdirpy(fhdir)

for s in samples:
    if s.sex == "M":
        males += 1
    elif s.sex == "F":
        females += 1
    else:
        print(s._label, " missing data")

print("Males:", males)
print("Females:", females)


for s in samples:  # save plots showing data trims
    fname = f"full_{s._label}.png"
    fig, axs = plt.subplots(2, figsize=(22,8), dpi=150)
    fig.suptitle(f"{s._label} last test\n")

    axs[0].plot(s.data[s.last_i]["force"])
    axs[0].plot(s.last_pull["force"], color=colors[-1])
    axs[0].set_title(str(s.last_i+1) + "0% force [g]")

    axs[1].plot(s.data[s.last_i]["height"])
    axs[1].plot(s.last_pull["height"], color=colors[-1])
    axs[1].set_title(str(s.last_i+1) + "0% height [px]")

    fig.tight_layout()
    plt.savefig(str(fhdir / fname))
    # plt.show()
    plt.close()
