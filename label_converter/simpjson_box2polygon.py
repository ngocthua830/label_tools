import os
import json
from pathlib import Path

if __name__=="__main__":
    infopath = "labels_simjson"
    outfopath = "simjson_seg"
    
    infopath = Path(infopath)
    outfopath = Path(outfopath)
    
    clslist = []
    for fpath in infopath.iterdir():
        print(fpath)
        if fpath.suffix != ".json":
            continue
        with open(fpath) as f:
            c = json.load(f)
        
        polygon = []
        for box in c["bboxes"]:
            print(box)
            cls = box["class_name"]
            
            if cls not in clslist:
                clslist.append(cls)
            
            conf = 1.0
            x1 = box["x1"]
            y1 = box["y1"]
            x2 = box["x2"]
            y2 = box["y2"]
            points = [{"x": x1, "y": y1}, {"x": x2, "y": y1}, {"x": x2, "y": y2}, {"x": x1, "y": y2}]
            polygon.append({"class_name": cls, "points": points, "conf": 1.0})
        
        simpjson = c
        simpjson["bboxes"] = []
        simpjson["polygon"] = polygon
        with open(( outfopath / fpath.name), "w") as fo:
            json.dump(simpjson, fo)
    
    # save classes.txt
    with open((outfopath / "classes.txt"), "w") as f:
        for cls in clslist:
            f.write("%s\n" %cls)











