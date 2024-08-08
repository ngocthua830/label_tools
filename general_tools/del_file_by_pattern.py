import os
import glob

inpath = "ThuannData"
patterns = ["_1.jpg", "_2.jpg", "_3.jpg", "_4.jpg", "_5.jpg", "_6.jpg", "_7.jpg", "_8.jpg", "_9.jpg"]

for p in patterns:
    for fpath in glob.glob(os.path.join(inpath, "*%s*" %p)):
        print(fpath)
        os.remove(fpath)        
        

