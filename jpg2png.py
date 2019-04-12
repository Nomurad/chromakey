import os, glob
import argparse
import cv2
import numpy as np

img_name_default = "test"
extension = "." + "png"

def main(img_name, extension):
    jpg = cv2.imread(img_name+extension, -1)
    png = cv2.imwrite(img_name+".png", jpg)


#コマンドライン引数を取得
parser = argparse.ArgumentParser()

#引数設定
parser.add_argument("--image")
parser.add_argument("--extension")

args = parser.parse_args()

if __name__ == "__main__":
    
    if args.image:
        img_name = args.image
    else:
        img_name = img_name_default

    if args.extension:
        extension = args.extension
    
    # filename = img_name + extension
    main(img_name, extension)