# -*- coding: utf-8 -*-
import cv2
import numpy as np


img_g = cv2.imread(r'gfp/g.jpg')
g1, g2 = (2, 382), (409, 382)
img_f = cv2.imread(r'gfp/f1.png')
f1, f2 = (396, 630), (1041, 630)  # (80, 423), (497, 423)
img_p = cv2.imread(r'gfp/p.jpg')
p1, p2 = (35, 245), (156, 245)

SQRT3 = np.sqrt(3)
SQRT3OVER2 = SQRT3 / 2.


def QFL2xy(QFL, scale):
    b, c, a = QFL

    a *= scale/100
    b *= scale/100
    c *= scale/100

    x = a + b/2.
    y = SQRT3OVER2 * b
    # print(scale)
    return x, y


def show(img, p1, p2, QFL, name):
    scale = abs(p1[0]-p2[0])
    o = p1

    x0, y0 = QFL2xy(QFL, scale)
    x, y = o[0]+x0, o[1]-y0
    point = (int(x), int(y))

    show_img = np.copy(img)
    cv2.circle(show_img, point, 5, (0, 0, 200), thickness=-1)
    # cv2.namedWindow(name)
    # show_img = cv2.resize(show_img, (show_img.shape[1] // 2, show_img.shape[0] // 2))
    if 'F' in name:
        show_img = cv2.resize(show_img, None, fx=0.5, fy=0.5)
    cv2.imshow(name, show_img)


def show_on_gfp(QFL):
    show(img_g, g1, g2, QFL, 'Garzanti')
    show(img_f, f1, f2, QFL, 'Folk')
    show(img_p, p1, p2, QFL, 'Pettijohn')

def show_on_g(QFL):
    show(img_g, g1, g2, QFL, 'Garzanti')

def show_on_f(QFL):
    show(img_f, f1, f2, QFL, 'Folk')

def show_on_p(QFL):
    show(img_p, p1, p2, QFL, 'Pettijohn')


if __name__ == '__main__':
    show_on_gfp((25, 25, 50))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

