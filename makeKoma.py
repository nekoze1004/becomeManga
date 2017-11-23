import cv2
import numpy as np

imgWidth = 960
imgHeight = 540
wakuWid = 5
Height = imgHeight * 4 + wakuWid * 10
Width = imgWidth + wakuWid * 2


def isWaku(i, j):
    if i < wakuWid or i >= imgHeight * 4 + wakuWid * 4 or \
                    j < wakuWid or j >= imgWidth + wakuWid:
        return True
    else:
        return isNakaWaku(i, j)


def isNakaWaku(i, j):
    if imgHeight + wakuWid * 2 >= i > imgHeight + wakuWid or \
                                            imgHeight * 2 + wakuWid * 3 >= i > imgHeight * 2 + wakuWid * 2 or \
                                            imgHeight * 3 + wakuWid * 4 >= i > imgHeight * 3 + wakuWid * 3:
        return True


if __name__ == "__main__":

    koma = np.zeros((int(Height), int(Width)))

    """for i in range(koma.shape[0]):
        for j in range(koma.shape[1]):
            if isWaku(i, j):
                koma[i, j] = 0
            else:
                koma[i, j] = 255"""

    print(koma.shape)

    cv2.imshow("koma", koma)
    cv2.imwrite("./Koma/koma_half_black.png", koma)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
