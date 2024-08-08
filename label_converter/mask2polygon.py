import os

import cv2
import numpy as np
from imantics import Polygons, Mask
from simplification.cutil import (
    simplify_coords,
    simplify_coords_idx,
    simplify_coords_vw,
    simplify_coords_vw_idx,
    simplify_coords_vwp,
)

def convert(mask, epsilon=5.0):
    polygons = Mask(mask).polygons()
    
    new_polygons = []
    for i in range(len(polygons.points)):
        polygon = simplify_coords(polygons.points[i], epsilon)
        polygon = polygon[1:]
        new_polygon = []
        for x, y in list(polygon):
            new_polygon.append((int(x), int(y)))
        new_polygons.append(new_polygon)
    
    return new_polygons

if __name__=="__main__":
    mask = np.load("mask.npy")
    polygons = convert(mask)
    print(polygons)
    
    # visualize
    h, w = mask.shape
    img = np.zeros((h,w,3))
    img.fill(255)
    for polygon in polygons:
        img = cv2.polylines(img, np.int32([polygon]), True, (255,0,0), 3)
        for x, y in polygon:
            img = cv2.circle(img, (x,y), radius=5, color=(255, 0, 255), thickness=-1)
    
    cv2.imwrite("polygons.jpg", img)
