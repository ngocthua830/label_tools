import os
import json
from datetime import datetime
from pathlib import Path

def write_class_list(fo, class_list):
    for cls in class_list:
        cls = cls.rstrip()
        fo.write('\t\t\t<label>\n')
        fo.write('\t\t\t\t<name>%s</name>\n' %cls)
        fo.write('\t\t\t</label>\n')

def write_info(fo, class_list):
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    
    fo.write('<?xml version="1.0" encoding="utf-8"?>\n')
    fo.write('<annotations>\n')
    fo.write('\t<version>1.1</version>\n')
    fo.write('\t<meta>\n')
    
    fo.write('\t\t<labels>\n')
    write_class_list(fo, class_list)
    fo.write('\t\t</labels>\n')
    
    fo.write('\t\t<dumped>%s</dumped>\n' %dt_string)
    
    fo.write('\t</meta>\n')

def simpjson2cvat(simpjsonpath, cvatpath):
    fo = open(cvatpath, "w")
    with open(simpjsonpath/"classes.txt") as clsf:
        class_list = clsf.readlines()
    write_info(fo, class_list)
    
    for i, fpath in enumerate(simpjsonpath.iterdir()):
        print(fpath)
        
        if fpath.suffix != ".json":
            continue
        
        with open(fpath) as jf:
            jc = json.load(jf)
#        print(jc)
        
        fo.write('<image id="%s" name="%s" width="%s" height="%s">\n' %(i, fpath.name, jc["image_width"], jc["image_height"]))
        for polygon in jc["polygon"]:
            print(polygon)
            points = ""
            for point in polygon["points"]:
                x = point["x"]
                y = point["y"]
                points += "%s,%s;" %(x, y)
            fo.write('<polygon label="%s" source="manual" occluded="0" points="%s" z_order="0"></polygon>\n' %(polygon["class_name"], points.rstrip(";")))
        fo.write('</image>\n')

    fo.write('</annotations>')
    fo.close()

if __name__=="__main__":
    simpjsonpath = Path("page_0_seg_simpjson")
    cvatpath = Path("page_0_seg_cvat.xml")
    
    simpjson2cvat(simpjsonpath, cvatpath)
        
        
