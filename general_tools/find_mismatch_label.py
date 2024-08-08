import os

from pathlib import Path

ext = "json"
without_img_ext = False
imgpath = "images_500"
labelpath = "simpjson_500"

imgpath = Path(imgpath)
labelpath = Path(labelpath)

f1 = open("mismatch_label.txt", "w")
f2 = open("mismatch_img.txt", "w")

for fpath in imgpath.iterdir():
    if without_img_ext:
        labelname = "%s.%s" %(fpath.stem, ext)
    else:
        labelname = "%s.%s" %(fpath.name, ext)
    
    lpath = os.path.join(labelpath, labelname)
    if os.path.exists(lpath):
        print(fpath.name, lpath)
        f1.write("%s\n" %fpath.name)
    else:
        print("miss ", fpath.name)

for fpath in labelpath.iterdir():
    imgname = "%s" %fpath.stem
    ipath = os.path.join(imgpath, imgname)
    if os.path.exists(ipath):
        print(fpath.name, ipath)
        f2.write("%s\n" %fpath.name)

f1.close()
f2.close()
