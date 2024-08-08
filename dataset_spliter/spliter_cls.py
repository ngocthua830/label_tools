import os
import random
import glob
import shutil

def create_split_list(imgpath, train_percent, test_percent, val_percent):
    imglist = os.listdir(imgpath)
    imgnum = len(imglist)

    train_imgnum = int(imgnum * train_percent / 100)
    test_imgnum = int(imgnum * test_percent / 100)
    val_imgnum = int(imgnum * val_percent / 100)

    test_imglist = random.sample(imglist, test_imgnum)
    val_imglist = random.sample(imglist, val_imgnum)
    train_imglist = []
    for imgname in imglist:
        if imgname not in test_imglist:
            train_imglist.append(imgname)

    return train_imglist, val_imglist, test_imglist

def process(flist, fopath, outpath):
    for fname in flist:
        fpath = os.path.join(fopath, fname)
        nfpath = os.path.join(outpath, fname)
        shutil.copy(fpath, nfpath)

def split_folder(fopath, train_path, valid_path, test_path, train_percent, val_percent, test_percent):
    train_imglist, val_imglist, test_imglist = create_split_list(fopath, train_percent, test_percent, val_percent)
    process(train_imglist, fopath, train_path)
    process(val_imglist, fopath, valid_path)
    process(test_imglist, fopath, test_path)

def split(fopath, train_percent, test_percent, val_percent):
    if train_percent + test_percent + val_percent != 100:
        assert "percent sum not == 100"

    train_path = "train"
    valid_path = "valid"
    test_path = "test"
    if not os.path.exists(train_path):
        os.mkdir(train_path)
    if not os.path.exists(valid_path):
        os.mkdir(valid_path)
    if not os.path.exists(test_path):
        os.mkdir(test_path)
    
    for dname in os.listdir(fopath):
        if not os.path.exists(os.path.join(train_path, dname)):
            os.mkdir(os.path.join(train_path, dname))
        if not os.path.exists(os.path.join(valid_path, dname)):
            os.mkdir(os.path.join(valid_path, dname))
        if not os.path.exists(os.path.join(test_path, dname)):
            os.mkdir(os.path.join(test_path, dname))
        
        dpath = os.path.join(fopath, dname)
        split_folder(dpath, os.path.join(train_path, dname), os.path.join(valid_path, dname), os.path.join(test_path, dname), train_percent, val_percent, test_percent)
    


if __name__ == "__main__":
    fopath = "images"
    train_percent = 70
    test_percent = 10
    val_percent = 20
    split(fopath, train_percent, test_percent, val_percent)
