import os
import uuid
from pathlib import Path
from shutil import copyfile

inpath = "images_noinhan"
labelpath = "simpjson_noinhan"
outpath = "images_noinhan"
labeloutpath = "simpjson_noinhan"
REMOVE_OLD_FILE = True

inpath = Path(inpath)
outpath = Path(outpath)
labelpath = Path(labelpath)
labeloutpath = Path(labeloutpath)

def gen_uuid():
    return str(uuid.uuid4())

if __name__=="__main__":
    for fpath in inpath.iterdir():
        print(fpath)
        new_name = gen_uuid()
        new_fpath = outpath / str("%s%s" %(new_name, fpath.suffix))
        label_fpath = labelpath / str("%s.json" %fpath.stem)
        label_new_fpath = labeloutpath / str("%s.json" %new_name)
    #    print(new_fpath)
        copyfile(fpath, new_fpath)
        copyfile(label_fpath, label_new_fpath)
        if REMOVE_OLD_FILE:
            os.remove(fpath)
            os.remove(label_fpath)
