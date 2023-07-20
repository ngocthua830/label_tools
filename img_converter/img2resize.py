import os

import cv2

INPATH = "train_ulabeled"
OUTPATH = "ntrain_ulabeled"
img_width = 200
img_height = 200

if not os.path.exists(OUTPATH):
    os.mkdir(OUTPATH)

for cls in os.listdir(INPATH):
    clspath = os.path.join(INPATH, cls)
    nclspath = os.path.join(OUTPATH, cls)
    if not os.path.exists(nclspath):
        os.mkdir(nclspath)
    for fname in os.listdir(clspath):
        print(cls, fname)
        fpath = os.path.join(clspath, fname)
        nfpath = os.path.join(nclspath, fname)
        img = cv2.imread(fpath)
        img = cv2.resize(img, (200, 200))
        cv2.imwrite(nfpath, img)
