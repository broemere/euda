# @author: broemere
# created: 7/18/2022
"""
Collect last pull csv data and images
"""
from elib import *
runinit()
timer = runstartup()

raw_images = rawdir / "raw_images"
samples = loadinterm("1-samples")

for s in samples:
    raw_image_dir = raw_images / s.date.replace("-","_")
    last_test = s.data[-1]
    s.last_i = len(s.data) - 1
    expected_length = (s.last_i + 1) * 500
    if abs(len(last_test)-expected_length) > 250:
        last_test = s.data[-2]
        s.last_i = len(s.data) - 2
        expected_length = (s.last_i + 1) * 500
    test_length = expected_length / 5

    s.start = int(expected_length - test_length - 1)
    s.stop = int(s.start + (test_length/2) + 1)
    s.last_pull = last_test[s.start:s.stop]
    s.live_imgs = []
    s.live_img_names = []

    for timestamp in s.last_pull.stamp:
        img_file = format(timestamp, ".3f") + ".png"
        img_path = raw_image_dir / img_file
        img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)

        s.live_imgs.append(img)
        s.live_img_names.append(img_file)


writeinterm("1-live-imgs", samples)

