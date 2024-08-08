import os
import cv2

inpath = "images_500"
outpath = "images_500_resized"

nw = 720

for fname in os.listdir(inpath):
    print(fname)
    
    fpath = os.path.join(inpath, fname)
    img = cv2.imread(fpath)
    h,w, _ = img.shape
    
    nh = int(nw*h/w) 
    
    nimg = cv2.resize(img, (nw, nh))
    
    nfpath = os.path.join(outpath, fname)
    cv2.imwrite(nfpath, nimg)
