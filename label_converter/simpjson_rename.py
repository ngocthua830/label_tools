import os
import json

from pathlib import Path

if __name__=="__main__":
    infopath = Path("simpjson")
    outfopath = Path("simpjson")
    
    mapping_cls = {"coquanbanhanh": "line", "loaivanban": "line", "sokyhieu": "line", "ngaybanhanh": "line", "nguoiky": "line"}
    for fpath in infopath.iterdir():
        print(fpath)
        if fpath.suffix != ".json":
            continue
        with open(fpath) as f:
            c = json.load(f)
        
        polygons = []
        for poly in c["polygon"]:
            cls = poly["class_name"]
            if cls in mapping_cls.keys():
                poly["class_name"] = mapping_cls[cls]
                polygons.append(poly)
            else:
                polygons.append(poly)
                
        c["polygon"] = polygons
        
        fopath = outfopath / fpath.name
        with open(fopath, "w") as f:
            json.dump(c, f)
    
    clslist = []
    with open(infopath / "classes.txt") as f:
        c = f.readlines()
    for cls in c:
        cls = cls.strip()
        if cls not in mapping_cls.keys():
            if cls not in clslist:
                clslist.append(cls)
        elif mapping_cls[cls] not in clslist:
            clslist.append(mapping_cls[cls])
    with open((outfopath / "classes.txt"), "w") as f:
        for cls in clslist:
            f.write("%s\n" %cls)







