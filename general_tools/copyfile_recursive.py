import os
import glob
from shutil import copyfile

#inpath = "public/fake"
#outpath = "images/fake"
inpath = "public/real"
outpath = "images/real"

ipath = os.path.join(inpath, "*/*")
for fpath in glob.glob(ipath, recursive=True):
    fname = fpath.split("/")[-1]
    print(fname)
    opath = os.path.join(outpath, fname)
    copyfile(fpath, opath)
