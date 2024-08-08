import os
from pathlib import Path
from shutil import copyfile

inpath = "images"
outpath = "nfc_images"

patterns = ["*_6_0*"]

for fpath in Path(inpath).rglob(patterns[0]):
    print(fpath)
    
    nfpath = Path(outpath) / fpath.name
    copyfile(fpath, nfpath)


