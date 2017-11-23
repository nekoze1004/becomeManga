import cv2
import numpy as np
import os
from numba import jit

imgWidth = 960
imgHeight = 540
wakuWid = 5
Height = imgHeight * 4 + wakuWid * 6
Width = imgWidth + wakuWid * 2

path = r"./SS"


@jit
def imgMasking(base, mask, startX, startY):
    print("bb")
    y = startY
    """print(base.shape)
    print(mask.shape)"""
    for i in range(mask.shape[0]):
        for j in range(mask.shape[1]):
            print("mask:" + str(i) + "," + str(j))
            print("base:" + str(startX) + "," + str(startY) + "\n")
            base[startX, startY] = mask[i, j]
            startY += 1
        startY = y
        startX += 1


if __name__ == "__main__":
    koma = cv2.imread("./Koma/koma_half_black.png")
    print(koma.shape)

    dir = os.listdir(path)
    img_list = []

    limit = 0
    for file in dir:
        if limit == 4:
            break
        print(file)
        img = cv2.imread(os.path.join(path, file))
        img_mini = cv2.resize(img, (int(imgWidth), int(imgHeight)))
        img_list.append(img_mini)
        limit += 1

    count = 0
    startX = int(wakuWid)
    startY = int(wakuWid)
    for im in range(len(img_list)):
        print("aaa")
        imgMasking(koma, img_list[im], startX, startY)
        cv2.imshow(str(im), koma)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        count += 1
        startX += imgHeight + wakuWid * count
        print(str(count) + ":" + str(startX))

    cv2.imshow("result", koma)
    cv2.imwrite("result.png", koma)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
