# @author: broemere
# created: 7/18/2022
"""
~~~Description~~~
"""
from elib import *
runinit()
timer = runstartup()

samples = loadinterm("1-thresh-solved")

def rotate_image(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result

angles = np.arange(-10, 11)

for s in samples:
    print(s._label)
    s.th_imgs = []
    s.heights = []

    for img in s.live_imgs:
        if np.max(img) in [0, 1]:
            thresh1 = deepcopy(img)
        else:
            ret, thresh1 = cv2.threshold(deepcopy(img), s.th_best, 255, cv2.THRESH_BINARY)
        canv = img_cleanup(thresh1)
        s.th_imgs.append(canv)

        horiz_sum = np.sum(canv, axis=1)
        widths = horiz_sum[horiz_sum > 0]
        height = len(widths)
        s.heights.append(height)

    del s.live_imgs

    for img in s.side:
        vert_sum = np.sum(img, axis=0)
        thickness = len(vert_sum[vert_sum > 0])

        # plus biggest average height

        # find angle of largest moment of inertia

        # draw a line and find average difference between number of pixels on each side in each row

        print(thickness)

    break


writeinterm("1-geometry", samples)
