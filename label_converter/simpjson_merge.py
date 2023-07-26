import os
import json
from pathlib import Path

if __name__=="__main__":
    infopath1 = "labels"
    infopath2 = "labels2_simp"
    outfopath = "labels_combine"
    cls_to_merge = []
    
    infopath1 = Path(infopath1)
    infopath2 = Path(infopath2)
    outfopath = Path(outfopath)
    
    clslist = []
    
    # load class list from classes.txt
    if os.path.exists(infopath1 / "classes.txt"):
        with open((infopath1 / "classes.txt"), "r") as f:
            c = f.readlines()
        for cls in c:
            clslist.append(cls.strip())
    if os.path.exists(infopath2 / "classes.txt"):
        with open((infopath2 / "classes.txt"), "r") as f:
            c = f.readlines()
        for cls in c:
            if cls not in clslist:
                clslist.append(cls.strip())
    
    for fpath1 in infopath1.iterdir():
        print(fpath1.name)
        if fpath1.suffix != ".json":
            continue
        
        fpath2 = infopath2 / fpath1.name
        fopath = outfopath / fpath1.name
#        print(fpath1, fpath2, fopath)
        with open(fpath1) as f1:
            c1 = json.load(f1)
        with open(fpath2) as f2:
            c2 = json.load(f2)
        
        print(c2)     
#        print("class list 1", c1["class_list"] if "class_list" in c1 else "")
#        print("class list 2", c2["class_list"] if "class_list" in c2 else "")
        
        # merge box
        for box in c2["bboxes"]:
            if box["class_name"] not in clslist:
                clslist.append(box["class_name"])
            
            if cls_to_merge == []:
                c1["bboxes"].append(box)
            elif box["class_name"] in cls_to_merge:
                c1["bboxes"].append(box)
        
        # merge polygon
        for poly in c2["polygon"]:
            if poly["class_name"] not in clslist:
                clslist.append(poly["class_name"])
            
            if cls_to_merge == []:
                c1["polygon"].append(poly)
            elif poly["class_name"] in cls_to_merge:
                c1["polygon"].append(poly)
        
        with open(fopath, "w") as fo:
            json.dump(c1, fo)
    
    # save classes.txt
    with open((outfopath / "classes.txt"), "w") as f:
        for cls in clslist:
            f.write("%s\n" %cls)










