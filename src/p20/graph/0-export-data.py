# @author: broemere
# created: 8/3/2022
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

alphabet = "abcdefghijklmnopqrstuvwxyz"
numset = set()

drop = ["07D", "31C", "31D", "34C", "34D", "36C", "36D"]
drop = []

for s in samples:
    numset.add(s._no)
numset = sorted(numset)

plt.figure()
ddict = {"M": [], "F":[]}
for s in samples:
    no_idx = list(numset).index(s._no)
    s.letter = alphabet[no_idx].upper()
    if s._type == "C" and s._label not in drop:
        x = s.stretch_interp
        y = s.stress_range
        if y[0] == 2:
            y = y - 1
        if y[0] == 0:  # this is hacky and should be fixed somewhere else?
            x = x - x[0] + 1
        elif y[0] == 1:
            y = np.arange(0, np.max(y)+1)
            x = [1] + x
        elif y[0] < 0:
            y = y[y>0]
            x = x[-len(y):]
            x = x - x[0] + 1
        df = pd.DataFrame(np.column_stack((x, y)),
                          columns=[s.letter+" stretch", s.letter + " stress"])
        ddict[s.sex].append(df)
        plt.scatter(x,y, marker=".")
plt.show()
plt.close()

for i in ["F", "M"]:
    ddict[i] = pd.concat(ddict[i], axis=1, ignore_index=False)
toexcel(ddict, "p20-stress-stretch-mf-cells-all", ddict.keys())


plt.figure()
ddict = {"M": [], "F":[]}
for s in samples:
    no_idx = list(numset).index(s._no)
    s.letter = alphabet[no_idx].upper()
    if s._type == "D" and s._label not in drop:
        x = s.stretch_interp
        y = s.stress_range
        if y[0] == 2:
            y = y - 1
        if y[0] == 0:  # this is hacky and should be fixed somewhere else?
            x = x - x[0] + 1
        elif y[0] == 1:
            y = np.arange(0, np.max(y)+1)
            x = [1] + x
        elif y[0] < 0:
            y = y[y>0]
            x = x[-len(y):]
            x = x - x[0] + 1
        df = pd.DataFrame(np.column_stack((x, y)),
                          columns=[s.letter+" stretch", s.letter + " stress"])
        ddict[s.sex].append(df)
        plt.scatter(x,y, marker=".")
plt.show()
plt.close()

for i in ["F", "M"]:
    ddict[i] = pd.concat(ddict[i], axis=1, ignore_index=False)
toexcel(ddict, "p20-stress-stretch-mf-decell-all", ddict.keys())



#%%
samples2 = loadinterm("1-injected-front")

for s in samples2:
    no_idx = list(numset).index(s._no)
    s.letter = alphabet[no_idx].upper()

samples = samples2 + samples

ddict = {"M": [], "F":[]}
for s in samples:
    no_idx = list(numset).index(s._no)
    s.letter = alphabet[no_idx].upper()
    if s._type == "C" and s._label not in drop:

        x = np.array(s.heights_one_gram)*CAMERA_SCALE

        df = pd.DataFrame(x,
                          columns=[s.letter+" height"])
        ddict[s.sex].append(df)


for i in ["F", "M"]:
    ddict[i] = pd.concat(ddict[i], axis=1, ignore_index=False)
toexcel(ddict, "p20-ring-size-mf-cells-all", ddict.keys())

ddict = {"M": [], "F":[]}
for s in samples:
    no_idx = list(numset).index(s._no)
    s.letter = alphabet[no_idx].upper()
    if s._type == "D" and s._label not in drop:

        x = np.array(s.heights_one_gram)*CAMERA_SCALE

        df = pd.DataFrame(x,
                          columns=[s.letter+" height"])
        ddict[s.sex].append(df)


for i in ["F", "M"]:
    ddict[i] = pd.concat(ddict[i], axis=1, ignore_index=False)
toexcel(ddict, "p20-ring-size-mf-decell-all", ddict.keys())

