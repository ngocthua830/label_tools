import os
from pathlib import Path

inpath = "input.txt"
infopath = "images"

with open(inpath) as f:
    c = f.readlines()

for line in c:
    line = line.strip()
    print(line)
    fpath = os.path.join(infopath, line)
    if os.path.exists(fpath):
        os.remove(fpath)
