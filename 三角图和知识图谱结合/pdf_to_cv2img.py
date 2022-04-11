import fitz
import os
import cv2
from PIL import Image
from io import BytesIO
import numpy as np
"""
输入: pdf文件路径
输出: pdf按页截图的列表
"""
def pdf_to_cv2img_list(pdf_path):

    pdf = fitz.open(pdf_path)
    cv2img_list = []

    for pg, page in enumerate(pdf):

        # 缩放系数
        zoom = 2
        mat = fitz.Matrix(zoom, zoom)
        pix = page.getPixmap(matrix=mat, alpha=False)  # alpha = 是否使用透明背景

        pix1 = fitz.Pixmap(pix, 0) if pix.alpha else pix
        img_data = pix1.getImageData("png")
        bytes_stream = BytesIO(img_data)
        img = Image.open(bytes_stream)
        # img.show()  # 通过系统默认方式打开图片
        cv2img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
        cv2img_list.append(cv2img)

    return cv2img_list


if __name__ == "__main__":
    doc_dir = r'documents/'

    doc_list = os.listdir(doc_dir)

    print('文件列表:', doc_list)
    print('文件数量:', len(doc_list))

    for i, doc_name in enumerate(doc_list):

        if doc_name[-4:].lower() == r'.pdf':

            pdf_path = doc_dir + doc_name
            # pdf_name = doc_name[:-4]  # 删除末尾扩展名
            # if len(pdf_name) > 50:
            #     pdf_name = pdf_name[:50].strip()  # 截断过长文件名 去除可能的末尾空格 # 过长的文件名会导致保存失败 windows能接受的最长路径长度为255
            print(i, ' ', doc_name)
            cv2img_list = pdf_to_cv2img_list(pdf_path)

            for i, img in enumerate(cv2img_list):
                cv2.imshow('%s  page:%d' % (doc_name, i+1), img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
        else:
            print("未知文件或目录:", doc_name)
