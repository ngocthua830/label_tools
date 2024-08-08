import os
from shutil import copyfile

txt = "fake.txt"
src_folder = "selfie_images"
dst_folder = "tmp"

with open(txt, "r") as f:
    c = f.readlines()

for fname in c:
    fname = fname.strip()
    print(fname)
    src_path = os.path.join(src_folder, fname)
    dst_path = os.path.join(dst_folder, fname)
    copyfile(src_path, dst_path)
    

