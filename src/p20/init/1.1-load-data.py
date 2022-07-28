# @author: broemere
# created: 7/9/2022
"""
Initialize samples from csv files + metadata, get all first and side images
"""
from elib import *
runinit()
timer = runstartup()

samples = []

metadata = pd.read_excel(rawdir / "P20 animal workbook.xlsx")

for pth, dirs, files in os.walk(rawdir):
    for i, f in enumerate([f for f in files if f.lower().endswith(".xls")]):
        #print(f)
        sample_no = f[:2]
        sample_type = f[2]
        label = sample_no + sample_type
        if label == "07C" or label == "08C":
            continue
        pull = f[3:5]
        pull_index = int(pull[0]) - 1
        mtime = os.path.getmtime(Path(pth) / f)
        datedir = os.path.split(pth)[1]
        csv = pd.read_csv(Path(pth, f), sep="\t", names=["force", "height", "width", "stamp"])
        if label not in [s._label for s in samples]:
            meta_row = metadata[metadata["Mouse #"] == "P20-0" + sample_no]
            sex = meta_row["Sex"]
            sex = "F" if sex.empty else sex.item()  # TRUE?
            s = ns(_label=label, _no=sample_no, _type=sample_type, date=datedir, sex=sex)
            s.data = []
            s.mtimes = []
            #s.front = []
            #s.frontfiles = []
            s.first = []
            s.side = []
            samples.append(s)
        else:
            s = getsample(samples, label)

        if len(s.data) == pull_index:
            s.data.append([])
            s.mtimes.append([])
            #s.front.append([])
            #s.frontfiles.append([])
            s.first.append([])
            s.side.append([])
        s.data[pull_index] = csv
        s.mtimes[pull_index] = mtime

t0_list = list(np.concatenate([[s.data[i]['stamp'][0] for i in range(len(s.data))] for s in samples]).flat)

for pth, dirs, files in os.walk(rawdir):
    for i, f in enumerate([f for f in files if f.lower().endswith(".png")]):
        parentdir = os.path.split(pth)[1]
        if parentdir in [s.date for s in samples]:
            #print(f)
            sample_no = f[:2]
            sample_type = f[2]
            label = sample_no + sample_type
            pull = f[3:5]
            pull_index = int(pull[0]) - 1
            mtime = os.path.getmtime(Path(pth) / f)
            match = None
            match_diff = 1e8
            for s in samples:
                for j in s.mtimes:
                    diff = j - mtime
                    if diff > 0 and diff < match_diff:
                        match = (s._label, s.mtimes.index(j))
                        match_diff = diff
            #print(match)
            #s = getsample(samples, match[0])
            #img = cv2.imread(str(Path(pth) / f), cv2.IMREAD_GRAYSCALE)
            #s.front[match[1]] = img
            #s.frontfiles[match[1]] = str(Path(pth) / f)

        upperdir = os.path.split(os.path.split(pth)[0])[1]
        if upperdir == "raw_images":
            if f[:-4].endswith("old"):
                continue
            if float(f[:-4]) in t0_list:
                imgdate = parsedate(parentdir.replace("_", "-"))
                for s in samples:
                    t0s = [s.data[i]['stamp'][0] for i in range(len(s.data))]
                    if imgdate == parsedate(s.date) and float(f[:-4]) in t0s:
                        img = cv2.imread(str(Path(pth) / f), cv2.IMREAD_GRAYSCALE)
                        s.first[t0s.index(float(f[:-4]))] = img
                        print(s._label + str(t0s.index(float(f[:-4]))))


    for i, f in enumerate([f for f in files if f.lower().endswith(".jpg")]):
        parentdir = os.path.split(pth)[1]
        if parentdir == "phone":
            #print(f)
            mtime = os.path.getmtime(Path(pth) / f)
            match = None
            match_diff = 1e8
            for s in samples:
                for j in s.mtimes:
                    diff = j - mtime
                    if diff > 0 and diff < match_diff:
                        match = (s._label, s.mtimes.index(j))
                        match_diff = diff
            #print(match, "side")
            s = getsample(samples, match[0])
            phone_binary_path = rawdir / "phone_binary"
            img = cv2.imread(str(Path(phone_binary_path) / f), cv2.IMREAD_GRAYSCALE)
            canv = img_cleanup(img)
            s.side[match[1]] = canv


#%%

for i, s in enumerate(samples):
    if len(s.first[0]) == 0:
        continue
    #s.frontcrop = []
    #print(round((i+1) / len(samples) * 100))
    # for img, template in zip(s.front, s.first):
    #     w, h = template.shape[::-1]
    #     res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    #     min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    #     top_left = max_loc
    #     crop = img[top_left[1]:top_left[1]+h, top_left[0]:top_left[0]+w]
    #     s.frontcrop.append(crop)
    # del s.front

samples = sorted(samples, key=lambda x: x._label)
timer.check()

#%%
writeinterm("1-samples", samples)