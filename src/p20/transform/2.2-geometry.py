# @author: broemere
# created: 7/28/2022
"""
Threshold and safely crop live images; realign all images; hard crop first and side images
"""
from elib import *
from mayavi import mlab
runinit()
timer = runstartup()
samples = loadinterm("2-clean")

for s in samples:
    print(s.th_best)
    block = np.ones((s.front_first.shape[1], s.side_first.shape[1], s.front_first.shape[0]))
    for layer in range(block.shape[1]):
        block[:, layer, :] = block[:, layer, :] * s.front_first.swapaxes(0,1)
    for layer in range(block.shape[0]):
        block[layer, :, :] = block[layer, :, :] * s.side_first.swapaxes(0,1)
    s.voxel_first = block.astype(np.uint8)

    s.voxel_one_gram = []
    for i, img in enumerate(s.front_one_gram):
        block = np.ones((img.shape[1], s.side_one_gram[i].shape[1], img.shape[0]))
        for layer in range(block.shape[1]):
            block[:, layer, :] = block[:, layer, :] * img.swapaxes(0,1)
        for layer in range(block.shape[0]):
            block[layer, :, :] = block[layer, :, :] * s.side_one_gram[i].swapaxes(0,1)
        s.voxel_one_gram.append(block.astype(np.uint8))

    s.heights = []
    for img in s.th_imgs:
        horiz_sum = np.sum(img, axis=1)
        widths = horiz_sum[horiz_sum > 0]
        height = len(widths)
        s.heights.append(height)

        img_crop = img_hardcrop(img)

        dims = img_crop.shape
        side_img = s.side[s.last_i]
        width = np.round((dims[0]/side_img.shape[0])*side_img.shape[1]).astype(int)
        side_img_scaled = cv2.resize(side_img, (width, dims[0]), interpolation=cv2.INTER_NEAREST)


    s.heights_one_gram = []
    for img in s.front_one_gram:
        horiz_sum = np.sum(img, axis=1)
        widths = horiz_sum[horiz_sum > 0]
        height = len(widths)
        s.heights_one_gram.append(height)

    plt.figure()
    plt.scatter(np.arange(len(s.heights)), s.last_pull["height"], marker=".", label="LabVIEW")
    plt.scatter(np.arange(len(s.heights)), s.heights, marker=".", label="Goal Seeked")
    plt.ylabel("Height [px]")

    plt.show()
    plt.close()




#writeinterm("2-voxels", samples)