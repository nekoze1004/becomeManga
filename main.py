import cv2, datetime, sys
import numpy as np
from tkinter.filedialog import *

# 画像一枚のサイズ
imgWidth = 960
imgHeight = 540

# 枠の太さ
wakuWid = 5

# コマの数
komakazu = 4

# レイアウト1のサイズ
Height1 = imgHeight * komakazu
Width1 = imgWidth

# レイアウト2のサイズ
Height2 = imgHeight * 2
Width2 = imgWidth * 2


# レイアウト1の枠線の位置
def isWaku1(i, j):
    if i < wakuWid or i >= Height1 - wakuWid or \
                    j < wakuWid or j >= Width1 - wakuWid:
        return True
    else:
        return isNakaWaku1(i, j)


# レイアウト1の枠線の位置　なぜ分けた？
def isNakaWaku1(i, j):
    if imgHeight + wakuWid / 2 >= i > imgHeight - wakuWid / 2 or \
                                            imgHeight * 2 + wakuWid / 2 >= i > imgHeight * 2 - wakuWid / 2 or \
                                            imgHeight * 3 + wakuWid / 2 >= i > imgHeight * 3 - wakuWid / 2:
        return True


# レイアウト2の枠線の位置
def isWaku2(i, j):
    if i < wakuWid or i >= Height2 - wakuWid or \
                    j < wakuWid or j >= Width2 - wakuWid:
        return True
    else:
        return isNakawaku2(i, j)


# レイアウト2の枠線の位置
def isNakawaku2(i, j):
    if imgHeight + wakuWid / 2 >= i > imgHeight - wakuWid / 2 or \
                                    imgWidth + wakuWid / 2 >= j > imgWidth - wakuWid / 2:
        return True


# レイアウト1で画像を繋げていく関数
def imgMasking1(base, mask, startX, startY):
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


# レイアウト2で画像を繋げていく関数
def imgMasking2(base, mask, startX, startY):
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


# GUIでファイル選択する　ファイルパスが入ったリストが返される
def fileSelects():
    fType = [("*.jpg", "*.png")]
    iDir = os.path.abspath(os.path.dirname(__file__) + "/SS")
    print(iDir)
    filename = askopenfilenames(filetypes=fType, initialdir=iDir)
    filelist = list(filename)
    print(filelist)
    return filelist


# ファイルの保存とプレビューを行う関数
def fileWrite(koma):
    today = datetime.datetime.today()
    print(today.strftime("%Y%m%d%H%M%S"))
    cv2.imshow("result", koma)
    cv2.imwrite("./result/" + today.strftime("%Y%m%d%H%M%S") + ".png", koma)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 初期化？　保存先と探索先が無いなら作る
def initialize():
    if not (os.path.exists("./result")):
        os.mkdir("./result")

    if not (os.path.exists("./SS")):
        os.mkdir("./SS")


# めいん　ごちゃごちゃしすぎ　書き直したい
if __name__ == "__main__":
    print(__file__)
    initialize()
    print("コマのタイプを選べ 1 or 2")
    komaType = input(">>> ")

    # 画像を入れるリスト
    img_list = []

    # 画像を4つ選ばせる 3つでも5つでもダメだ きっちり4つ
    limit = 0
    for i in range(komakazu):
        # 冗長？
        if limit == komakazu:
            break
        filelist = fileSelects()
        # fileSelects()から帰ってきたリストの中身を回す
        for file in filelist:
            # コマ数と同じ数の画像を取得したら抜け出す
            if limit == komakazu:
                break
            img = cv2.imread(file)
            # リサイズしてる　スクショの元サイズだとデカすぎて見づらい
            img_mini = cv2.resize(img, (int(imgWidth), int(imgHeight)))
            img_list.append(img_mini)
            limit += 1

    # レイアウト1
    if int(komaType) == 1:
        print("1")

        # 受け皿を作る
        koma1 = np.empty((Height1, Width1, 3), np.uint8)

        startX = 0
        startY = 0  # こいつ要らないかもしれない
        for im in range(len(img_list)):
            # startXは1080→2160→3240となるはず
            startX = imgMasking1(koma1, img_list[im], startX, startY)

        # 枠線つける
        for i in range(koma1.shape[0]):
            for j in range(koma1.shape[1]):
                if isWaku1(i, j):
                    koma1[i, j] = 0

        # ファイルを保存して終了する
        fileWrite(koma1)
        sys.exit()

    # レイアウト2
    elif int(komaType) == 2:
        print("2")
        # 受け皿を作る
        koma2 = np.empty((Height2, Width2, 3), np.uint8)

        # 画像を中央で4分割して、
        # 第一象限、第二象限、第四象限、第三象限の順に画像を配置する
        count = 0
        # 第一象限
        startX = 0
        startY = imgWidth
        for im in range(len(img_list)):
            imgMasking2(koma2, img_list[im], startX, startY)
            count += 1
            if count == 1:
                # 第二象限
                startX = imgHeight
                startY = imgWidth
            elif count == 2:
                # 第四象限
                startX = 0
                startY = 0
            elif count == 3:
                # 第三象限
                startX = imgHeight
                startY = 0

        # 枠線をつける
        for i in range(koma2.shape[0]):
            for j in range(koma2.shape[1]):
                if isWaku2(i, j):
                    koma2[i, j] = 0

        # ファイルを保存して終了する
        fileWrite(koma2)
        sys.exit()
