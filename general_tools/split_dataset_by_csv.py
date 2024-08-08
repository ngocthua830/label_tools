import os
from shutil import copyfile

flabel = "label.csv"
spliter = ","
indir = "videos"
outdir = "./"
with open(flabel, "r") as f:
    c = f.readlines()

for l in c[1:]:
    l = l.strip()
    fname, label = l.split(spliter)
    print(fname, label)
    odir = os.path.join(outdir, label)
    if not os.path.exists(odir):
        os.mkdir(odir)
    fpath = os.path.join(indir, fname)
    fpath1 = os.path.join(odir, fname)
    print(fpath, fpath1)
    copyfile(fpath, fpath1)


