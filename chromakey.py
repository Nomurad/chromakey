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
    try:
        mask_para = np.loadtxt("mask_setting.txt", dtype=np.uint8)
        print(mask_para)
    except:
        raise FileExistsError("mask_setting.txt is not found.")

    lower_color = np.array([70, 40, 0])
    upper_color = np.array([130, 255, 255])

    img = cv2.imread(file_name, cv2.IMREAD_COLOR)
    # img = img/255
    if img is None:
        raise FileNotFoundError("Reading image file"+ file_name +" failed.")


    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_color, upper_color)   #maskを設定
    inv_mask = cv2.bitwise_not(mask)    #maskを反転
    result_hsv = cv2.bitwise_and(img, img, mask=inv_mask)

    # result = cv2.cvtColor(result_hsv, cv2.COLOR_HSV2BGR)

    cv2.imwrite("chromakey_"+file_name, result_hsv)

    img = cv2.imread("chromakey_"+file_name, 1)
    # img = cv2.imread(file_name, cv2.IMREAD_UNCHANGED)
    # print(img)
    print(img.shape)
    
    
    h, w = img.shape[:2]
    mask = np.zeros((h+2, w+2), dtype=np.uint8)

    flags = 4 | 255 << 8 | cv2.FLOODFILL_MASK_ONLY
    print(bin(flags))

    if img.shape[-1] < 4:
        rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    else:
        rgba = img

    cv2.floodFill(img, mask, seedPoint=(3,3), newVal=(0,0,255), flags=flags)
    # cv2.imshow("mask",mask)

    mask = mask[1:-1, 1:-1]
    rgba[mask==255] = 0
    cv2.imwrite("masked.png", rgba)

    # cv2.imshow("image",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # idx_black = np.where(img[:,:,3] != 0)




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

    main(img_name)
