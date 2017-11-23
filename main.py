import cv2
import numpy as np
import os
from numba import jit
import datetime
from tkinter.filedialog import *
import sys

imgWidth = 960
imgHeight = 540
wakuWid = 5
komakazu = 4
Height1 = imgHeight * komakazu
Width1 = imgWidth

Height2 = imgHeight * 2
Width2 = imgWidth * 2

path = r"./SS"


def isWaku1(i, j):
    if i < wakuWid or i >= Height1 - wakuWid or \
                    j < wakuWid or j >= Width1 - wakuWid:
        return True
    else:
        return isNakaWaku1(i, j)


def isNakaWaku1(i, j):
    if imgHeight + wakuWid / 2 >= i > imgHeight - wakuWid / 2 or \
                                            imgHeight * 2 + wakuWid / 2 >= i > imgHeight * 2 - wakuWid / 2 or \
                                            imgHeight * 3 + wakuWid / 2 >= i > imgHeight * 3 - wakuWid / 2:
        return True


def isWaku2(i, j):
    if i < wakuWid or i >= Height2 - wakuWid or \
                    j < wakuWid or j >= Width2 - wakuWid:
        return True
    else:
        return isNakawaku2(i, j)


def isNakawaku2(i, j):
    if imgHeight + wakuWid / 2 >= i > imgHeight - wakuWid / 2 or \
                                    imgWidth + wakuWid / 2 >= j > imgWidth - wakuWid / 2:
        return True


@jit
def imgMasking1(base, mask, startX, startY):
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


def imgMasking2(base, mask, startX, startY):
    print("cc")
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


def fileSelects():
    fType = [("*.jpg", "*.png")]
    iDir = os.path.abspath(os.path.dirname(__file__ + "./SS"))
    filename = askopenfilenames(filetypes=fType, initialdir=iDir)
    filelist = list(filename)
    print(filelist)
    return filelist


def fileWrite(koma):
    today = datetime.datetime.today()
    print(today.strftime("%Y%m%d%H%M%S"))
    cv2.imshow("result", koma)
    cv2.imwrite("./result/" + today.strftime("%Y%m%d%H%M%S") + ".png", koma)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    print("コマのタイプを選べ 1 or 2")
    komaType = input(">>> ")

    dir = os.listdir(path)
    img_list = []

    limit = 0
    for i in range(komakazu):
        if limit == komakazu:
            break
        filelist = fileSelects()
        for file in filelist:
            if limit == komakazu:
                break
            img = cv2.imread(file)
            img_mini = cv2.resize(img, (int(imgWidth), int(imgHeight)))
            img_list.append(img_mini)
            limit += 1
    print("aaa")
    print(type(komaType))
    if int(komaType) == 1:
        print("1")
        koma1 = np.empty((Height1, Width1, 3), np.uint8)
        print(koma1.shape)

        startX = 0
        startY = 0
        for im in range(len(img_list)):
            startX = imgMasking1(koma1, img_list[im], startX, startY)
            print(startX)

        for i in range(koma1.shape[0]):
            for j in range(koma1.shape[1]):
                if isWaku1(i, j):
                    koma1[i, j] = 0

        fileWrite(koma1)
        sys.exit()

    elif int(komaType) == 2:
        koma2 = np.empty((Height2, Width2, 3), np.uint8)
        print(koma2.shape)

        count = 0
        startX = 0
        startY = imgWidth
        for im in range(len(img_list)):
            imgMasking2(koma2, img_list[im], startX, startY)
            count += 1
            if count == 1:
                startX = imgHeight
                startY = imgWidth
            elif count == 2:
                startX = 0
                startY = 0
            elif count == 3:
                startX = imgHeight
                startY = 0
            print(count)

        for i in range(koma2.shape[0]):
            for j in range(koma2.shape[1]):
                if isWaku2(i, j):
                    koma2[i, j] = 0

        fileWrite(koma2)
        sys.exit()
