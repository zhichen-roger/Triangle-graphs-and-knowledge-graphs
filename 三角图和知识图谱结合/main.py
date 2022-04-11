import cv2
import os
import sys
print('importing cv2_drawer')
import cv2_drawer
print('importing pdf_to_cv2img')
import pdf_to_cv2img


if __name__ == "__main__":
    # doc_dir = 'gfp/'
    doc_dir = r'documents/'  # 待检测文件所在文件夹
    doc_list = os.listdir(doc_dir)

    print('文件列表:', doc_list)
    print('文件数量:', len(doc_list))

    for i, doc_name in enumerate(doc_list):
        print()
        print(i, doc_name)
        if doc_name[-4:].lower() == r'.pdf':

            pdf_path = doc_dir + doc_name
            cv2img_list = pdf_to_cv2img.pdf_to_cv2img_list(pdf_path)

            for page, img in enumerate(cv2img_list):
                window_name = '%s  page:%d' % (doc_name, page+1)
                print('page:', page+1)

                QFL_list = cv2_drawer.run(img, window_name)
                if QFL_list:
                    print('QFL data list:', QFL_list)

        elif doc_name[-4:].lower() in ('.jpg', '.png'):
            img_path = doc_dir + doc_name
            img = cv2.imread(img_path)
            window_name = doc_name

            QFL_list = cv2_drawer.run(img, window_name)
            if QFL_list:
                print('QFL data list:', QFL_list)

        else:
            print("未知文件或目录:", doc_name)
    # 程序退出
    print('documents文件夹内所有文件标注完毕 按任意键退出')
    print()
    os.system("pause")
    sys.exit()