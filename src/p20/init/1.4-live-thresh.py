# @author: broemere
# created: 7/18/2022
"""
Auto threshold live images for each sample
"""
from elib import *
runinit()
timer = runstartup()

samples = loadinterm("1-live-imgs")
thresh_range = np.arange(40, 100)

print(f"Completion time: {int(np.around((len(samples)*14))/60)} min")

for i, s in enumerate(samples):  # 15 sec per
    print(s._label)
    s.errors = []
    for th in thresh_range:
        heights = []
        for img in s.live_imgs:
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
    tprint(f"{round((i + 1) / len(samples) * 100)}%")

    # graph(np.arange(len(s.last_pull)), s.last_pull.height)
    # graph(np.arange(len(heights)), heights)

timer.check(True)
writeinterm("1-auto-thresh", samples)
