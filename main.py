import cv2, datetime, sys
import numpy as np
from tkinter.filedialog import *
from tqdm import tqdm

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

# 1枚目の画像かどうか
firstImg_Flg = False

# 一回目の起動か
first = True


# レイアウト1の枠線の位置
def isWaku1(i, j):
    if i < wakuWid or i >= Height1 - wakuWid or \
                    j < wakuWid or j >= Width1 - wakuWid:
        return True
    else:
        return isNakaWaku1(i, j)


# レイアウト1の枠線の位置　なぜ分けた？
def isNakaWaku1(i, j):
    for k in range(komakazu):
        if imgHeight * k + wakuWid / 2 >= i > imgHeight * k - wakuWid / 2:
            return True


# レイアウト1で画像を繋げていく関数
def imgMasking1(base, mask, startX, startY):
    y = startY
    """print(base.shape)
    print(mask.shape)"""
    for i in tqdm(range(mask.shape[0])):
        for j in range(mask.shape[1]):
            """print("mask:" + str(i) + "," + str(j))
            print("base:" + str(startX) + "," + str(startY) + "\n")"""
            base[startX, startY] = mask[i, j]
            startY += 1
        startY = y
        startX += 1
    return startX


# GUIでファイル選択する　ファイルパスが入ったリストが返される
def fileSelects():
    fType = [("*.jpg", "*.png")]
    iDir = os.path.abspath(os.path.dirname(__file__) + "/SS")
    filename = askopenfilenames(filetypes=fType, initialdir=iDir)
    filelist = list(filename)
    print(filelist)
    return filelist


# ファイルの保存とプレビューを行う関数
def fileWrite(koma):
    today = datetime.datetime.today()
    # print(today.strftime("%Y%m%d%H%M%S"))
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


# 入力された文字列はexitではないか
def isNotExit(Mess):
    global first
    print(Mess)
    inputStr = input(">>> ")
    if inputStr == "e":
        print("exit")
        return False
    elif inputStr == "c":
        config()
        return True
    else:
        print("loop")
        return True


def printConfig():
    global imgHeight, imgWidth, Height1, Width1, wakuWid, komakazu
    print("-----現在の設定-----")
    print("縦:" + str(imgHeight))
    print("横:" + str(imgWidth))
    print("マンガサイズ:" + str(Height1) + "," + str(Width1))
    print("枠の太さ:" + str(wakuWid))
    print("コマの数:" + str(komakazu))
    print("--------------------")


def config():
    global imgHeight, imgWidth, Height1, Width1, wakuWid, komakazu

    flg = True
    while (flg):
        print("""設定画面\n画像サイズ変更：i\n枠の太さ変更：w\nコマの数:k\n設定の確認:m\n終わる：end""")
        com = input(">>> ")
        if com == "i":
            print("縦")
            inputH = input(">>> ")
            imgHeight = int(inputH)
            print("横")
            inputW = input(">>> ")
            imgWidth = int(inputW)
            Height1 = imgHeight * komakazu
            Width1 = imgWidth
            printConfig()
        elif com == "w":
            print("枠の太さ")
            inputWW = input(">>> ")
            wakuWid = int(inputWW)
            printConfig()
        elif com == "k":
            print("コマの数")
            inputK = input(">>> ")
            komakazu = int(inputK)
            Height1 = imgHeight * komakazu
            printConfig()
        elif com == "m":
            printConfig()
        elif com == "end":
            flg = False
        else:
            print("出直せ")


# めいん　ごちゃごちゃしすぎ　書き直したい
if __name__ == "__main__":
    initialize()

    while (isNotExit("止めるならe 設定はc")):

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

                # 1枚目のサイズに合わせる
                # つもりだけどうまくいかない
                if firstImg_Flg:
                    imgHeight = img.shape[0]
                    imgWidth = img.shape[1]
                    print(imgHeight)
                    print(imgWidth)
                    Height1 = imgHeight * komakazu
                    Width1 = imgWidth
                    print(Height1)
                    print(Width1)
                    firstImg_Flg = False

                # リサイズしてる　スクショの元サイズだとデカすぎて見づらい
                img_mini = cv2.resize(img, (int(imgWidth), int(imgHeight)))
                img_list.append(img_mini)
                limit += 1

        # 受け皿を作る
        koma1 = np.empty((Height1, Width1, 3), np.uint8)

        startX = 0
        startY = 0  # こいつ要らないかもしれない
        for im in range(len(img_list)):
            # startXは1080→2160→3240となるはず
            startX = imgMasking1(koma1, img_list[im], startX, startY)

        # 枠線つける
        for i in tqdm(range(koma1.shape[0])):
            for j in range(koma1.shape[1]):
                if isWaku1(i, j):
                    koma1[i, j] = 0

        # ファイルを保存して終了する
        fileWrite(koma1)

        # 1枚目かどうかのフラグをリセットする
        firstImg_Flg = False

    # exitって打たれたら終了する(書かなくていいのでは)
    sys.exit()
