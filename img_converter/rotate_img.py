import os
from PIL import Image

inpath = "images"
outpath = "images_-90"
degree = -90
for fname in os.listdir(inpath):
    fpath = os.path.join(inpath, fname)
    print(fpath)
    img = Image.open(fpath)
    img = img.convert('RGB')
    img_90 = img.rotate(degree, expand=True)
    fname_woext = '.'.join(fname.split(".")[:-1])
    npath = os.path.join(outpath, '%s_%s.jpg' %(fname_woext, str(degree)))
    img_90.save(npath)
