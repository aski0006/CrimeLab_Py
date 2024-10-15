"""
Author: Asaki0019 3031007372@qq.com
Date: 2024-05-15 19:48:23
LastEditors: Asaki0019 3031007372@qq.com
LastEditTime: 2024-05-15 23:39:03
FilePath: \Python\Crime\Trans_Doc_To_TXT.py
"""

import os
import win32com.client
from tqdm import tqdm


def doc_to_text(doc_path, txt_path):
    # 创建Word应用程序对象
    word_app = win32com.client.Dispatch("Word.Application")

    # 打开Word文档
    doc = word_app.Documents.Open(doc_path)

    # 读取文档内容并存储到txt文件中
    doc_content = doc.Content.Text
    with open(txt_path, "w", encoding="utf-8") as txt_file:
        txt_file.write(doc_content)

    # 关闭Word文档和应用程序对象
    doc.Close()
    word_app.Quit()


def batch_convert_doc_to_txt(doc_folder, txt_folder):
    # 获取文件夹中的所有doc文件列表
    doc_files = [
        filename for filename in os.listdir(doc_folder) if filename.endswith(".doc")
    ]

    # 使用tqdm显示进度条
    with tqdm(total=len(doc_files), desc="Converting", unit="file") as pbar:
        # 遍历文件夹中的所有doc文件
        for filename in doc_files:
            # 构建doc文件的完整路径
            doc_path = os.path.join(doc_folder, filename)

            # 构建对应的txt文件路径
            txt_filename = filename[:-4] + ".txt"  # 移除.doc扩展名，添加.txt扩展名
            txt_path = os.path.join(txt_folder, txt_filename)

            # 调用函数进行转换
            doc_to_text(doc_path, txt_path)

            # 更新进度条
            pbar.update(1)


# 指定输入的doc文件夹路径和输出的txt文件夹路径
doc_folder_path = "D:\下载\机器学习大项目\刑事案件"
txt_folder_path = "D:\Code\Python\Crime\Txt"

# 如果输出文件夹不存在，则创建
if not os.path.exists(txt_folder_path):
    os.makedirs(txt_folder_path)

# 调用函数进行批量转换
batch_convert_doc_to_txt(doc_folder_path, txt_folder_path)
