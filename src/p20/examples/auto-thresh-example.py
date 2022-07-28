# @author: broemere
# created: 7/26/2022
import cv2
import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy


def make_video(filepath, data, fps):
    """ filepath - where the video will be saved
        data - list of images to make into video
        fps - frames per second"""
    if len(data[0].shape) == 3:
        size = data[0].shape[::-1][1:3]
        is_color = True
    else:
        size = data[0].shape[::-1]
        is_color = False
    print(size)
    video = cv2.VideoWriter(str(filepath),
                            cv2.VideoWriter_fourcc(*"mp4v"),  # May need to try "xvid" or "divx"
                            fps, size, is_color)
    for img in data:
        video.write(img)
    cv2.destroyAllWindows()
    video.release()


def get_largest_object(img):
    """(img) Find largest object in binary image.
        TREE method.
        Deals with 0 and very small area contours
        Returns image with only biggest object"""
    approx_meth = cv2.CHAIN_APPROX_NONE
    cnts, hiers = cv2.findContours(img, cv2.RETR_TREE, approx_meth)
    areas = np.array([])
    cntarray = []
    for j in cnts:
        a = cv2.contourArea(j)
        if len(areas) < 1:
            areas = np.append(areas, a)
            cntarray.append(j)
        else:
            smlst = np.argmin(areas)
            if a > areas[smlst] or areas[smlst] == 0:
                areas = np.delete(areas, smlst)
                del cntarray[smlst]
                areas = np.append(areas, a)
                cntarray.append(j)
    cnt = cntarray[0]
    canv = cv2.drawContours(np.zeros(img.shape), [cnt], -1, 1, -1)
    return canv


def display(img, gray=False):
    fig = plt.figure(dpi=300, frameon=False)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    if gray:
        ax.imshow(img, cmap="gray")
    else:
        ax.imshow(img)
    plt.show()
    plt.close()


###################################################################################################

# Make video example

sample = loadinterm("1-live-imgs")[4]
filename = f"{sample._label}_ring_test.avi"
make_video(filename, sample.live_imgs, 5)


#%% ###############################################################################################

# Load video example

video = cv2.VideoCapture(filename)
frames = []

while True:
    ret, frame = video.read()  # ret is false if no more frames can be read
    if ret:
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frames.append(frame_gray)
    else:
        print("Done reading video")
        break

video.release()


#%% ###############################################################################################

# Box select region of interest

frames_roi = []

for frame in frames:
    frame_roi = frame[100:800, 50:150]
    frames_roi.append(frame_roi)

display(frames[-1][100:800, 50:150], True)


#%% ###############################################################################################

# Auto thresholding to maximize linear stretch and fit

thresh_range = np.arange(40, 100)  # Test threshold values from 40 to 100
kernel_size = 5

errors = []  # Error for each threshold value
# Error = RMSE / slope of height

for th in thresh_range:  # Check each thresh value
    print(th)
    heights = []
    for img in frames:  # Threshold each image in the video

        ret, thresh1 = cv2.threshold(deepcopy(img), th, 255, cv2.THRESH_BINARY)  # Threshold
        # Use deepcopy() when you want to avoid modifying the original
        opening = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, np.ones((kernel_size, kernel_size)))  # Clean up noise
        isolated_object = get_largest_object(opening)  # Remove extra garbage

        horiz_sum = np.sum(isolated_object, axis=1)  # Sum columns in x direction
        height = len(horiz_sum[horiz_sum > 0])  # height is the total non-zero pixels in the column
        heights.append(height)

    x = [0, len(heights)]  # dummy x values
    y = [heights[0], heights[-1]]  # initial and final heights
    coefficients = np.polyfit(x, y, 1)  # calculate m and b for y = mx + b
    polynomial = np.poly1d(coefficients)
    x_fitted = np.linspace(0, len(heights), len(heights))
    y_fitted = polynomial(x_fitted)

    resids = np.array(heights) - y_fitted  # residuals
    rmse = np.sqrt(np.sum((resids**2))/len(heights))
    error = (rmse / coefficients[1])  # minimize rmse and maximize slope of height change
    errors.append(error)


th_best = thresh_range[errors.index(np.min(errors))]  # best thresh value is the one with min error
print(th_best, "is the best threshold value")

###################################################################################################

# now do the final threshold with the best value

frames_threshed = []
heights = []

for img in frames:
    ret, thresh1 = cv2.threshold(deepcopy(img), th_best, 255, cv2.THRESH_BINARY)
    opening = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, np.ones((kernel_size, kernel_size)))
    isolated_object = (get_largest_object(opening) * 255).astype(np.uint8)
    # isolated_object is only 0 and 1 so multiply by 255 so we can see it
    horiz_sum = np.sum(isolated_object, axis=1)
    height = len(horiz_sum[horiz_sum > 0])
    heights.append(height)
    frames_threshed.append(isolated_object)

side_by_side = np.hstack((frames[-1], frames_threshed[-1]))
display(side_by_side, True)


x = [0, len(heights)]  # dummy x values
y = [heights[0], heights[-1]]  # initial and final heights

plt.figure(dpi=175)
plt.scatter(np.arange(len(heights)), heights, marker=".")
plt.plot(x, y, color="red")
plt.show()
plt.close()

