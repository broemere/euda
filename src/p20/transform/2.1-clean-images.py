# @author: broemere
# created: 7/28/2022
"""
Threshold and safely crop live images; realign all images; hard crop first and side images
"""
from elib import *
runinit()
timer = runstartup()
samples = loadinterm("1-auto-thresh")

for s in samples:
    print(s._label)
    s.th_imgs = []
    s.min_ynonzero = []
    s.max_ynonzero = []
    s.min_xnonzero = []
    s.max_xnonzero = []
    canvs = []

    for img in s.live_imgs:
        if np.max(img) in [0, 1]:
            thresh1 = deepcopy(img)
        else:
            thresh1 = img_thresh(img, s.th_best)
        canv = img_cleanup(thresh1)
        canvs.append(canv)
        y_nonzero, x_nonzero = np.nonzero(canv)
        s.min_ynonzero.append(np.min(y_nonzero))
        s.max_ynonzero.append(np.max(y_nonzero)+1)
        s.min_xnonzero.append(np.min(x_nonzero))
        s.max_xnonzero.append(np.max(x_nonzero)+1)

    s.ynonzero = (np.min(s.min_ynonzero), np.max(s.max_ynonzero))
    s.xnonzero = (np.min(s.min_xnonzero), np.max(s.max_xnonzero))

    approx_meth = cv2.CHAIN_APPROX_NONE
    cnts, hiers = cv2.findContours(canvs[-1], cv2.RETR_TREE, approx_meth)
    (x, y), (MA, ma), angle = cv2.fitEllipse(cnts[0])
    if angle > 90:
        angle = angle - 180

    for img in canvs:
        img_crop = img[s.ynonzero[0]:s.ynonzero[1], s.xnonzero[0]:s.xnonzero[1]]
        img_rot = img_rotate(img_crop, angle)
        s.th_imgs.append(img_rot)

    s.side_old = s.side
    s.side = []
    for img in s.side_old:
        img_crop = img_hardcrop(img_align(img))
        s.side.append(img_crop)

    s.first_old = s.first
    s.front_one_gram = []
    for img in s.first_old:
        thresh1 = img_thresh(img, s.th_best)
        canv = img_cleanup(thresh1)
        img_rot = img_rotate(canv, angle)
        img_crop = img_hardcrop(img_rot)
        s.front_one_gram.append(img_crop)

    s.front_first = img_hardcrop(s.th_imgs[0])

    s.side_one_gram = []
    for i, img in enumerate(s.side):
        dims = s.front_one_gram[i].shape
        width = np.round((dims[0]/img.shape[0])*img.shape[1]).astype(int)
        img_scaled = cv2.resize(img, (width, dims[0]), interpolation=cv2.INTER_NEAREST)
        s.side_one_gram.append(img_scaled)

    dims = s.front_first.shape
    width = np.round((dims[0] / s.side[-1].shape[0]) * s.side[-1].shape[1]).astype(int)
    s.side_first = cv2.resize(s.side[-1], (width, dims[0]), interpolation=cv2.INTER_NEAREST)

    del s.live_imgs

writeinterm("2-clean", samples)
