import os, glob
import argparse
import cv2
import numpy as np

img_name_default = "test"
extension = "." + "png"

def main(img_name):
    # dir_name = "."
    file_name = img_name + extension
    export_chromakey(file_name)


def export_chromakey(file_name):
    print("file name is ", file_name)

    #HSV形式で抜き出す色空間の指定
    lower_color = np.array([100, 110, 30])
    upper_color = np.array([120, 255, 255])

    img = cv2.imread(file_name)
    if img is None:
        raise FileNotFoundError("Reading image file failed.")

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower_color, upper_color)   #maskを設定
    inv_mask = cv2.bitwise_not(mask)    #maskを反転
    result = cv2.bitwise_and(img, img, mask=inv_mask)

    cv2.imwrite("chromakey_"+file_name, result)


#コマンドライン引数を取得
parser = argparse.ArgumentParser()

#引数設定
parser.add_argument("--image")

args = parser.parse_args()


if __name__ == "__main__":
    if args.image:
        img_name = args.image
    else:
        img_name = img_name_default

    main(img_name)
