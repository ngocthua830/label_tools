import os
import uuid
from pathlib import Path
from shutil import copyfile

inpath = "images_noinhan"
outpath = "images_noinhan"
REMOVE_OLD_FILE = True

inpath = Path(inpath)
outpath = Path(outpath)

def gen_uuid():
    return str(uuid.uuid4())

if __name__=="__main__":
    for fpath in inpath.iterdir():
        print(fpath)
        new_fpath = outpath / str("%s%s" %(gen_uuid(), fpath.suffix))
    #    print(new_fpath)
        copyfile(fpath, new_fpath)
        if REMOVE_OLD_FILE:
            os.remove(fpath)
