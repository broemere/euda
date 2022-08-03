# @author: broemere
# created: 7/29/2022
"""
Inject samples that have different shaped data
"""
from elib import *
runinit()
timer = runstartup()
samples = loadinterm("1-auto-thresh")

metadata = pd.read_excel(rawdir / "P20 animal workbook.xlsx")

for pth, dirs, files in os.walk(rawdir):
    for i, f in enumerate([f for f in files if f.lower().endswith(".xls")]):
        #print(f)
        sample_no = f[:2]
        sample_type = f[2]
        label = sample_no + sample_type
        if label == "07C" or label == "08C":
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
                s.front = []
                #s.frontfiles = []
                s.first = []
                s.side = []
                s.videos = []
                samples.append(s)
            else:
                s = getsample(samples, label)

            if len(s.data) == pull_index:
                s.data.append([])
                s.mtimes.append([])
                s.front.append([])
                #s.frontfiles.append([])
                s.first.append([])
                s.side.append([])
                s.videos.append([])
            s.data[pull_index] = csv
            s.mtimes[pull_index] = mtime


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
                s = getsample(samples, match[0])
                if s._label == "07C" or s._label == "08C":
                    print(match, "front")
                    img = cv2.imread(str(Path(pth) / f), cv2.IMREAD_GRAYSCALE)
                    s.front[match[1]] = img


    for i, f in enumerate([f for f in files if f.lower().endswith(".avi") or f.lower().endswith(".mkv")]):
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
                    diff = abs(j - mtime)
                    if diff < match_diff:
                        match = (s._label, s.mtimes.index(j))
                        match_diff = diff

            s = getsample(samples, match[0])
            print(match)
            print(f)
            video = cv2.VideoCapture(str(Path(pth) / f))
            fps = int(video.get(cv2.CAP_PROP_FPS))
            print(fps)
            print()
            frames = []
            counter = 0
            while True:
                ret, frame = video.read()  # ret is false if no more frames can be read
                if ret:
                    if counter == 0:
                        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        frame_gray[frame_gray == 1] = 0
                        frame_gray = img_hardcrop(frame_gray)[5:-5, 35:-35]
                        #thresh1 = img_thresh(deepcopy(frame_gray), s.th_best)
                        #canv = img_cleanup(thresh1)
                        frames.append(frame_gray)
                    counter += 1
                    if counter == fps/5:
                        counter = 0
                else:
                    break
            video.release()
            s.videos[match[1]] = frames


    for i, f in enumerate([f for f in files if f.lower().endswith(".jpg")]):
        parentdir = os.path.split(pth)[1]
        if parentdir == "phone":
            if f[4:12] == "20220426":
                print("found", f)
            mtime = os.path.getmtime(Path(pth) / f)
            match = None
            match_diff = 1e8
            for s in samples:
                for j in s.mtimes:
                    diff = j - mtime
                    if diff > 0 and diff < match_diff:
                        match = (s._label, s.mtimes.index(j))
                        match_diff = diff
            s = getsample(samples, match[0])
            if s._label == "07C" or s._label == "08C":
                print(match, "side")
                phone_binary_path = rawdir / "phone_binary"
                img = cv2.imread(str(Path(phone_binary_path) / f), cv2.IMREAD_GRAYSCALE)
                canv = img_cleanup(img)
                s.side[match[1]] = canv


timer.check(True)

writeinterm("1-injection", samples)

#%%

for s in samples:
    if s._label in ["07C", "08C"]:
        mkdirpy(intermdir / "obs-videos" / s._label)

        for i, frames in enumerate(s.videos):
            filepath = intermdir / "obs-videos" / s._label / str(i)
            mkdirpy(filepath)
            for j, f in enumerate(frames):
                #cv2.imwrite(str(filepath / (str(j) + ".png")), f)
                pass

#         s.allskips = []
#         for i, frames in enumerate(s.videos):
#             if len(frames) != 0:
#                 frame_last = np.zeros(frames[0].shape).astype(np.uint8)
#             s.allskips.append([])
#             for j, f in enumerate(frames):
#                 if frame_last.shape == f.shape:
#                     diff = np.sum(f - frame_last)
#                     if diff == 0:
#                         print(j, diff)
#                         s.allskips[i].append(j-1)
#                 frame_last = deepcopy(f)
#
#
#
#         for i, skips in enumerate(s.allskips):
#             if len(skips) > 0:
#
#                 skips = np.append(np.arange(0, np.min(skips)), skips)
#                 np.flip(skips)
#                 for j in skips:
#
#                     #del s.videos[i][j]
#                     pass
#
#
#
#         # GET ROI FOR FRONT
#
#         for img, template in zip(s.front, [frames[0] for frames in s.videos]):
#
#             pass
#
#
#
#
#         #SCALE
#
#         s.live_imgs = []
#
#         for i, frames in enumerate(s.videos):
#             s.live_imgs.append([])
#             front_height = s.front[i]
#             for j, f in enumerate(frames):
#                 #scale
#                 pass
#
#
#
#
#
#         for i, frames in enumerate(s.videos):
#             s.first[i] = frames[0]
#
#
#
#
#         #s.live_imgs = []
#
#
#
#
#     # for img, template in zip(s.front, s.first):
#     #     w, h = template.shape[::-1]
#     #     res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
#     #     min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
#     #     top_left = max_loc
#     #     crop = img[top_left[1]:top_left[1] + h, top_left[0]:top_left[0] + w]
#     #     s.frontcrop.append(crop)
#
# samples = sorted(samples, key=lambda x: x._label)
#
# #writeinterm("1-injection", samples)
#

#%%

thresh_range = np.arange(40, 100)

for s in samples:
    if s._label in ["07C", "08C"]:

        s.videos_fixed = []

        for i, frames in enumerate(s.videos):
            s.videos_fixed.append([])
            filepath = intermdir / "obs-videos" / s._label / str(i)
            for f in os.listdir(filepath):
                img = cv2.imread(str(filepath / f), cv2.IMREAD_GRAYSCALE)
                s.videos_fixed[i].append(img)
            s.videos_fixed[i] = s.videos_fixed[i][:len(s.data[i])]

        s.errors = []
        for th in thresh_range:
            heights = []
            for img in s.videos_fixed[-1]:
                if np.max(img) in [0, 1]:
                    continue
                ret, thresh1 = cv2.threshold(deepcopy(img), th, 255, cv2.THRESH_BINARY)
                canv = img_cleanup(thresh1)
                horiz_sum = np.sum(canv, axis=1)
                height = len(horiz_sum[horiz_sum > 0])  # absolute max height is best measure
                # vert_sum = np.sum(canv, axis=0)
                # height = np.max(vert_sum[vert_sum > 0])  # not better
                heights.append(height)

            x = [0, len(heights)]
            y = [heights[0], heights[-1]]
            coefficients = np.polyfit(x, y, 1)
            polynomial = np.poly1d(coefficients)
            x_fitted = np.linspace(0, len(heights), len(heights))
            y_fitted = polynomial(x_fitted)

            resids = np.array(heights) - y_fitted
            rmse = np.sqrt(np.sum((resids**2))/len(heights))
            error = (rmse / coefficients[1])  # minimize rmse and maximize slope
            s.errors.append(error)

        s.th_best = thresh_range[s.errors.index(np.min(s.errors))]

        print(s.th_best)




#%%

for s in samples:
   if s._label in ["07C", "08C"]:

        s.front_crop = []

        if s._label == "07C":
            s.videos_fixed[0].append(s.front[0])

        for img in s.front:
            s.front_crop.append(img[700:1350, 1300:1500])

        s.scales = []

        s.heights_one_gram = []


        for i, img in enumerate(s.front_crop):

            img_master = img_hardcrop(img_cleanup(img_thresh(img, s.th_best)))

            height = img_master.shape[0]

            s.heights_one_gram.append(height)


            img_small = img_hardcrop(img_cleanup(img_thresh(s.videos_fixed[i][0], s.th_best)))

            scale = height / img_small.shape[0]


            #front_crop = img_hardcrop(img_cleanup(img_thresh(img, s.th_best)))
            #height = front_crop.shape


            s.scales.append(scale)


            #video_rescale = template.shape / height


writeinterm("1-injected-front", [samples[-2], samples[-1]])








