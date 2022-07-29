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
CAMERA_SCALE = 1/39

drop = ["07D", "31C", "31D", "34C", "34D", "36C", "36D"]

cmap = cm.get_cmap("cool", 6)
colors = cmap(np.arange(0, cmap.N))

plt.figure(dpi=150)

for s in samples:
    if s._label in drop or s._type == "D":
        continue


        # plt.plot()
        # plt.scatter(np.arange(0, len(stretch)), stretch)
        # plt.scatter(np.arange(0, len(stretch)), stretch_lowess, marker=".")
        # plt.show()
        # plt.close()
        #
        # plt.plot()
        # plt.scatter(stretch, stress)
        # plt.scatter(stretch_lowess, stress, marker=".")
        # # plt.scatter(np.arange(0, len(s.data[s.last_i].force[s.start:s.stop])), s.data[s.last_i].force[s.start:s.stop])
        # # #plt.scatter(np.arange(0, len(w[:,1])), w[:,1], marker=".")
        # # #plt.scatter(stretch, force_lowess)
        # plt.show()
        # plt.close()

        s.heights_one_gram = []

        for img in s.front_one_gram:
            horiz_sum = np.sum(img, axis=1)
            widths = horiz_sum[horiz_sum > 0]
            height = len(widths)
            s.heights_one_gram.append(height)



        if s.sex == "M":
            #plt.scatter(stretch_lowess, s.stress, marker=".", color=colors[0], label="Male")

            plt.scatter(0, s.heights_one_gram[-1], marker=".", color=colors[0], label="Male")

        if s.sex == "F":
            #plt.scatter(stretch_lowess, s.stress, marker=".", color=colors[-1], label="Female")

            plt.scatter(1, s.heights_one_gram[-1], marker=".", color=colors[-1], label="Female")



        # break
        #
        #
        #
        #
        #     plt.plot()
        #     plt.scatter(np.arange(0, len(s.data[3].force)), s.data[3].force)
        #     plt.show()
        #     plt.close()

    plt.legend(*[*zip(*{l:h for h,l in zip(*plt.gca().get_legend_handles_labels())}.items())][::-1])
    #plt.ylim()
    plt.ylim(200, 500)
    plt.show()
    plt.close()