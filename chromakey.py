import os, glob
import argparse
import cv2
import numpy as np

img_name_default = "test.png"
fname = "masked.png"
# tablet_folder = "PC\Nexus 7\内部ストレージ\DCIM\Camera"
# extension = "." + "png"

def main(img_name, fname, mask_flag):
    # dir_name = "."
    file_name = listing_file()
    # file_name = img_name
    export_chromakey(file_name, fname, mask_flag)

def listing_file():
    if not os.path.exists("images/"):
        os.makedirs("images")
    files = (glob.glob("images/*"))
    for i, file in enumerate(files):
        fname_for_print = file.split("\\")[-1]
        print("[",i,"]",fname_for_print)

    fnum = input("select file No. > ")
    fnum = int(fnum)
    if fnum >= 0 and fnum <= len(files):
        print(files[fnum])
        return files[fnum]
    elif(fnum == -1):
        print(files[fnum])
        return files[fnum]
    else:
        print("failed.")


def export_chromakey(file_name , fname, mask_flag=0):
    print("file name is ", file_name)

    #HSV形式で抜き出す色空間の指定
    try:
        mask_para = np.loadtxt("mask_setting.txt", dtype=np.uint8)
        print(mask_para.shape)
    except:
        print("mask_setting.txt is not found.")
        lower_color = np.array([70, 40, 0])
        upper_color = np.array([130, 255, 255])

    if mask_flag == 0:
        lower_color = mask_para[0,:]
        upper_color = mask_para[1,:]
    elif mask_flag == 1:
        lower_color = mask_para[2,:]
        upper_color = mask_para[3,:]
    elif mask_flag == 2:
        lower_color = mask_para[4,:]
        upper_color = mask_para[5,:]

    print("lower ",lower_color, "  upper", upper_color)

    # print(lower_color, upper_color)

    img = cv2.imread(file_name, cv2.IMREAD_COLOR)
    # img = img/255
    if img is None:
        raise FileNotFoundError("Reading image file"+ file_name +" failed.")


    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_color, upper_color)   #maskを設定
    inv_mask = cv2.bitwise_not(mask)    #maskを反転
    result_hsv = cv2.bitwise_and(img, img, mask=inv_mask)

    # result = cv2.cvtColor(result_hsv, cv2.COLOR_HSV2BGR)

    cv2.imwrite("chromakey.png", result_hsv)

    img = cv2.imread("chromakey.png", 1)
    # img = cv2.imread(file_name, cv2.IMREAD_UNCHANGED)
    # print(hsv)
    # print(img)
    # print(img.shape)


    h, w = img.shape[:2]
    mask = np.zeros((h+2, w+2), dtype=np.uint8)

    flags = 4 | 255 << 8 | cv2.FLOODFILL_MASK_ONLY
    # print(bin(flags))

    if img.shape[-1] < 4:
        rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    else:
        rgba = img

    cv2.floodFill(img, mask, seedPoint=(30,30), newVal=(0,0,255), flags=flags)
    # cv2.imshow("mask",mask)

    mask = mask[1:-1, 1:-1]
    rgba[mask==255] = 0
    # cv2.imwrite(fname, rgba)
    cv2.imwrite(os.path.join("airplanes",fname), rgba)

    # cv2.imshow("image",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # idx_black = np.where(img[:,:,3] != 0)




#コマンドライン引数を取得
parser = argparse.ArgumentParser()

#引数設定
parser.add_argument("--image")
# parser.add_argument("--extension")
parser.add_argument("--name")
parser.add_argument("--backcolor")

args = parser.parse_args()


if __name__ == "__main__":

    mask_flag = 0

    if args.image:
        img_name = args.image
    else:
        img_name = img_name_default

    if args.name:
        fname = args.name + ".png"
    else:
        # fname = img_name_default
        fname = input("set output filename > ") + ".png"
        print(fname)

    if args.backcolor:
        mask_flag = int(args.backcolor)
        print("mask",mask_flag)

    # if args.extension:
    #     extension = args.extension

    main(img_name,fname, mask_flag)
