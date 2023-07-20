import os

from pdf2image import convert_from_bytes


def convert_path(inpath):
    images = convert_from_bytes(open(inpath, "rb").read())
    return images


def convert_bytes(inbytes):
    images = convert_from_bytes(inbytes)
    return images
