import cv2
import numpy as np
import sys
import webbrowser
import gfp
import requests
import time,os
from selenium import webdriver
from create_echarts_Stand import CreateEcharts

"""
输入: 图片
操作方法:
1.右键点击三角形左下底角
2.右键点击三角形右下底角
3.右键点击三角形上部顶角
4.左键点击三角形内部
5.步骤4重复多次后按空格结束本页标注
输出: 坐标点列表
"""


def p2l(p, p1, p2):
    # 计算点 p 到 (p1,p2两点表示的) 直线的距离
    # 对于两点坐标为同一点时,返回点与点的距离
    if p1 == p2:
        p_array = np.array(p)
        p1_array = np.array(p1)
        return np.linalg.norm(p_array - p1_array)
    else:
        A = p2[1] - p1[1]
        B = p1[0] - p2[0]
        C = (p1[1] - p2[1]) * p1[0] + (p2[0] - p1[0]) * p1[1]

        distance = abs(A * p[0] + B * p[1] + C) / (np.sqrt(A**2 + B**2))
        return distance


def xy2QFL(O, O1, O2, xy):
    Q = p2l(xy, O, O1) / p2l(O2, O, O1) * 100
    F = p2l(xy, O1, O2) / p2l(O, O1, O2) * 100
    L = p2l(xy, O, O2) / p2l(O1, O, O2) * 100

    return Q, F, L


def clear():
    global flag
    flag = 0

    global QFL_list
    QFL_list = []

    global img
    img = np.copy(original_img)

    global show_img
    # show_img = np.copy(original_img)
    M = np.float32([[1, 0, 0], [0, 1, f * 30]])
    show_img = cv2.warpAffine(original_img, M, (show_img.shape[1], show_img.shape[0]))
    cv2.imshow(window_name, show_img)


def clear_var():
    global flag
    flag = 0

    global show_img
    show_img = np.copy(original_img)
    cv2.imshow(window_name, show_img)


def show_ternary(O, O1, O2=None):
    """
    根据等边三角形 两底角坐标 作等边三角形
    根据等腰三角形 三个角坐标 作等腰三角形
    """
    if O2 == None:
        x = abs(O[0]-O1[0]) / 2. + min(O[0], O1[0])
        y = min(O[1], O1[1]) - SQRT3 / 2. * abs(O[0]-O1[0])
        O2 = (int(x), int(y))
    pts = np.array([O, O1, O2])
    cv2.polylines(show_img, [pts], True, (200, 0, 0), 4)  # 第三个参数表示是否封口,这里注意第二个参数外面必须再加一层中括号
    cv2.imshow(window_name, show_img)


def ispointinside(O, O1, O2, p):
    pts = np.array([O, O1, O2])

    return cv2.pointPolygonTest(pts, p, True) >= 0


def on_EVENT(event, x, y, flags, param):
    global flag
    global show_img
    global O, O1, O2
    global f
    global QFL_list
    searcher = CreateEcharts()
    if event == cv2.EVENT_LBUTTONDOWN and flag == 3 and ispointinside(O, O1, O2, (x, y)):
        # xy = "(%d,%d)" % (x, y)
        # QFL = XY_to_QFL(text_xy(O), text_xy(O1), text_xy(O2), text_xy((x,y)))

        QFL = Q, F, L = xy2QFL(O, O1, O2, (x, y))
        # TODO QFL数据输出
        print(QFL)
        key_name = ''
        # 分类
        if(F<10 and L<10):
            key_name = "Quartzose sandstone"

            print("MATCH p =()-[]-(:classfion{name:'Quartzose sandstone'}) return p ")
            print("Quartzose sandstone")
        elif(Q<10 and L<10):
            key_name = "Feldspathic sandstone"

            print("MATCH p =()-[]-(:classfion{name:'Feldspathic sandstone'}) return p ")
            print("Feldspathic sandstone")
        elif(Q<10 and F<10):
            key_name = "Lithic sandstone"

            print("MATCH p =()-[]-(:classfion{name:'Lithic sandstone'}) return p ")
            print("Lithic sandstone")
        elif(L>Q>F>10):
            key_name = "Feldspatho-quartzo-lithic sandstone"

            print("MATCH p =()-[]-(:classfion{name:'Feldspatho-quartzo-lithic sandstone'}) return p ")
            print("Feldspatho-quartzo-lithic sandstone")
        elif(F<10 and Q>L>10):
            key_name = "Litho-quartzose sandstone"

            print("MATCH p =()-[]-(:classfion{name:'Litho-quartzose sandstone'}) return p ")
            print("Litho-quartzose sandstone")
        elif(F>L>Q>10):
            key_name = "Quartzo-lithic-feldspatho sandstone"

            print("MATCH p =()-[]-(:classfion{name:'Quartzo-lithic-feldspatho sandstone'}) return p ")
            print("Quartzo-lithic-feldspatho sandstone")
        elif(F>Q>L>10):
            key_name = "Lithic-quartzo-feldspatho sandstone"

            print("MATCH p =()-[]-(:classfion{name:'Lithic-quartzo-feldspatho sandstone'}) return p ")
            print("Lithic-quartzo-feldspatho sandstone")
        elif(L<10 and F>Q>10):
            key_name = "Quartzo-feldspathic sandstone"

            print("MATCH p =()-[]-(:classfion{name:'Quartzo-feldspathic sandstone'}) return p ")
            print("Quartzo-feldspathic sandstone")
        elif(L<10 and Q>F>10):
            key_name = "Feldspatho-quartzose sandstone"

            print("MATCH p =()-[]-(:classfion{name:'Feldspatho-quartzose sandstone'}) return p ")
            print("Feldspatho-quartzose sandstone")
        elif(Q>F>L>10):
            key_name = "Lithic-feldspatho-quartzo sandstone"

            print("MATCH p =()-[]-(:classfion{name:'Lithic-feldspatho-quartzo sandstone'}) return p ")
            print("Lithic-feldspatho-quartzo sandstone")
        elif(L>F>Q>10):
            key_name = "Quartzo-feldspatho-lithic sandstone"

            print("MATCH p =()-[]-(:classfion{name:'Lithic-feldspatho-quartzo sandstone'}) return p ")
            print("Quartzo-feldspatho-lithic sandstone")
        elif(Q>L>F>10):
            key_name = "Feldspatho-lithic-quartzo sandstone"

            print("MATCH p =()-[]-(:classfion{name:'Feldspatho-lithic-quartzo sandstone'}) return p ")
            print("Feldspatho-lithic-quartzo sandstone")
        elif(Q<10 and L>F>10):
            key_name = "Feldspatho-lithic sandstone"

            print("MATCH p =()-[]-(:classfion{name:'Feldspatho-lithic sandstone'}) return p ")
            print("Feldspatho-lithic sandstone")
        elif(Q<10 and F>L>10):
            key_name = "Litho-feldspathic sandstone"

            print("MATCH p =()-[]-(:classfion{name:'Litho-feldspathic sandstone'}) return p ")
            print("Litho-feldspathic sandstone")
        elif(F<10 and L>Q>10):
            key_name = "Quartzo-lithic sandstone"

            print("MATCH p =()-[]-(:classfion{name:'Quartzo-lithic sandstone'}) return p ")
            print("Quartzo-lithic sandstone")
        elif(Q>95):
            key_name = "Quartzose sandstone"

            print("MATCH p =()-[]-(:classfion{name:'Quartzose sandstone'}) return p ")
            print("Quartzose sandstone")
        elif(F>25 and F>3*L):
            key_name = "Feldspathic sandstone"

            print("MATCH p =()-[]-(:classfion{name:'Feldspathic sandstone'}) return p ")
            print("Feldspathic sandstone")
        elif(L>25 and L>3*F):
            key_name = "Lithic sandstone"

            print("MATCH p =()-[]-(:classfion{name:'Lithic sandstone'}) return p ")
            print("Lithic sandstone")
        elif(5<F<25 and F>L):
            key_name = "Subarkose"

            print("MATCH p =()-[]-(:classfion{name:'Subarkose'}) return p ")
            print("Subarkose")
        elif(5<L<25 and L>F):
            key_name = "Sublitharenite"

            print("MATCH p =()-[]-(:classfion{name:'Sublitharenite'}) return p ")
            print("Sublitharenite")
        elif(Q<75 and 1<F/L<3):
            key_name = "Litho-feldspathic sandstone"

            print("MATCH p =()-[]-(:classfion{name:'Litho-feldspathic sandstone'}) return p ")
            print("Litho-feldspathic sandstone")
        elif(Q<75 and 1/3<F/L<1):
            key_name = "Feldspatho-lithic sandstone"

            print("MATCH p =()-[]-(:classfion{name:'Feldspatho-lithic sandstone'}) return p ")
            print("Feldspatho-lithic sandstone")
        elif(L<5 and F<5):
            key_name = "Quartz arenite"

            print("MATCH p =()-[]-(:classfion{name:'Quartz arenite'}) return p ")
            print("Quartz arenite")
        elif(F<L and L>25):
            key_name = "Lithic sandstone"

            print("MATCH p =()-[]-(:classfion{name:'Lithic sandstone'}) return p ")
            print("Lithic sandstone")
        elif(5<F<25 and F>L):
            key_name = "Subarkose"

            print("MATCH p =()-[]-(:classfion{name:'Subarkose'}) return p ")
            print("Subarkose")
        elif(5<L<25 and F<L):
            key_name = "Sublitharenite"

            print("MATCH p =()-[]-(:classfion{name:'Sublitharenite'}) return p ")
            print("Sublitharenite")
        elif(F>25 and F>L):
            key_name = "Feldspathic sandstone"

            print("MATCH p =()-[]-(:classfion{name:'Feldspathic sandstone'}) return p ")
            print("Feldspathic sandstone")
        elif(Q<95 and F>L):
            key_name = "Feldspathic wackes"

            print("MATCH p =()-[]-(:classfion{name:'Feldspathic wackes'}) return p ")
            print("Feldspathic wackes")
        elif(Q<95 and F<L):
            key_name = "Lithic wackes"

            print("MATCH p =()-[]-(:classfion{name:'Lithic wackes'}) return p ")
            print("Lithic wackes")
        elif(Q>95):
            key_name = "Quartz wackes"

            print("MATCH p =()-[]-(:classfion{name:'Quartz wackes'}) return p ")
            print("Quartz wackes")
        print("这里")



        #driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver_win32\chromedriver.exe')

        os.system('taskkill /F /IM chrome.exe')
        searcher.create_stone(key_name, "templates//echarts//render1" + ".html")
        chromePath = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chromePath))
        webbrowser.get('chrome').open(
            'http://localhost:63342/untitled1/demo%200.1.2/templates/echarts/render1.html',
            new=0, autoraise=True)

        QFL_list.append(QFL)

        # 显示分类情况
        #searcher.stone_classfion(key_name)
        list = searcher.stone_classfion(key_name)

        cv2.destroyWindow('Garzanti')
        cv2.destroyWindow('Folk')
        cv2.destroyWindow('Pettijohn')

        for i in range(len(list)):
            if (list[i] == "Garzanti"):
                gfp.show_on_g(QFL)
            elif (list[i] == "Folk"):
                gfp.show_on_f(QFL)
            elif (list[i] == 'Pettijohn'):
                gfp.show_on_p(QFL)
        #gfp.show_on_gfp(QFL)

        precision = 2
        # text_int = "(%d,%d,%d)" % QFL
        # text_float = "(%.2f,%.2f,%.2f)" % (round(Q, precision), round(F, precision), round(L, precision))
        text_QFL = "Q=%.2f F=%.2f L=%.2f" % (round(Q, precision), round(F, precision), round(L, precision))

        img = np.copy(show_img)  # 是否在画面保留上次点击的坐标点

        # cv2.circle(img, (x, y), 3, (0, 0, 255), thickness=-1)
        cv2.rectangle(img, (x-10, y-10), (x+10, y+10), (0, 0, 200), thickness=2)
        cv2.putText(img, text_QFL, (x-50, y+30), cv2.FONT_HERSHEY_PLAIN, 1.3, (0, 0, 0), thickness=2)
        cv2.imshow(window_name, img)

    elif event == cv2.EVENT_RBUTTONDOWN:
        if flag == 0:
            O = (x, y)
            print(O)
            cv2.circle(show_img, O, 3, (255, 0, 0), thickness=-1)
            cv2.imshow(window_name, show_img)
            flag += 1

        elif flag == 1:
            O1 = (x, O[1])  # 此处不接受O1的Y
            print(O1)
            cv2.circle(show_img, O1, 3, (255, 0, 0), thickness=-1)
            cv2.imshow(window_name, show_img)
            if x < O[0]:
                O, O1 = O1, O
            # show_ternary(O, O1)
            flag += 1

        elif flag == 2:
            O2 = ((O[0]+O1[0])//2, y)  # 此处不接收O2的X
            cv2.circle(show_img, O2, 3, (255, 0, 0), thickness=-1)
            cv2.imshow(window_name, show_img)
            show_ternary(O, O1, O2)
            flag += 1

        elif flag == 3:
            clear()

    elif event == cv2.EVENT_MOUSEWHEEL:
        clear_var()
        if flags > 0:  # 上移
            f += 1
        else:
            f += -1
        M = np.float32([[1, 0, 0], [0, 1, f * 30]])
        show_img = cv2.warpAffine(original_img, M, (show_img.shape[1], show_img.shape[0]))
        cv2.imshow(window_name, show_img)


def run(img, wn):
    global original_img, show_img
    original_img = np.copy(img)
    show_img = np.copy(img)

    global window_name
    window_name = wn

    global flag, f
    flag = 0  # 表示定位点数量 两个定位点确定一个等边三角形
    f = 0

    global SQRT3
    SQRT3 = np.sqrt(3)  # 根号三 ≈ 1.7320508075689

    global QFL_list
    QFL_list = []

    cv2.namedWindow(window_name)
    cv2.moveWindow(window_name, 0, 0)
    cv2.setMouseCallback(window_name, on_EVENT)
    cv2.imshow(window_name, img)

    while True:
        if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) <= 0:
            break
        key = cv2.waitKey(1000)
        #key = cv2.waitKey(1)
        if key == -1:
            continue
        elif key == 99:   # C键
            clear()
        elif key == ord(' '):
            break
        elif key == 27:
            sys.exit()

    cv2.destroyAllWindows()
    return QFL_list


if __name__ == "__main__":
    img_path = 'test.png'
    window_name = img_path
    img = cv2.imread(img_path)
    run(img, window_name)
