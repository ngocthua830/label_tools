import os
import shutil
inpath = "simpjson"
outpath = "simpjson1"

find_str = "_front"
replace_str = "_back"

for fname in os.listdir(inpath):
    fpath = os.path.join(inpath, fname)
    new_fname = fname.replace(find_str, replace_str)
    new_fpath = os.path.join(outpath, new_fname)
    print(fpath, new_fpath)
    shutil.copyfile(fpath, new_fpath)


