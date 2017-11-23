import cv2
import numpy as np
import os
from numba import jit

imgWidth = 960
imgHeight = 540
wakuWid = 5
Height = imgHeight * 4
Width = imgWidth

path = r"./SS"


@jit
def imgMasking(base, mask, startX, startY):
    print("bb")
    y = startY
    """print(base.shape)
    print(mask.shape)"""
    for i in range(mask.shape[0]):
        for j in range(mask.shape[1]):
            """print("mask:" + str(i) + "," + str(j))
            print("base:" + str(startX) + "," + str(startY) + "\n")"""
            base[startX, startY] = mask[i, j]
            startY += 1
        startY = y
        startX += 1
    return startX


if __name__ == "__main__":
    koma = np.empty((Height, Width, 3),np.uint8)
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
    startX = 0
    startY = 0
    for im in range(len(img_list)):
        print("aaa")
        startX = imgMasking(koma, img_list[im], startX, startY)
        print(startX)
        cv2.imshow(str(im), koma)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    cv2.imshow("result", koma)
    cv2.imwrite("result.png", koma)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
