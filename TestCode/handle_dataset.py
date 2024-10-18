"""
Author: Asaki0019 3031007372@qq.com
Date: 2024-05-28 18:49:17
LastEditors: Asaki0019 3031007372@qq.com
LastEditTime: 2024-05-28 22:55:21
FilePath: \Python\CrimeLab\TestCode\handlie_dataset.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
"""

import os
import re
import time
import openpyxl
import pandas as pd
from tqdm import tqdm

Test = 0
TestPrint = 1

Crimes = []
# Crimes_folder_path = r"D:\Code\Python\CrimeLab\TestCode\Crimes.txt"
Crimes_folder_path = r"D:\Code\Python\CrimeLab\Table\crimes_array.txt"
with open(Crimes_folder_path, "r", encoding="utf-8") as file:
    Crimes = [crime.strip() for crime in file.readlines()]


def create_excel_file(xlsx_data_file_path, Test):
    st = time.time()
    data = []
    files_skipped = []  # 用于记录无法存储到Excel中的文件路径
    base_path = ""
    if Test == 0:
        base_path = r"D:\Code\Python\CrimeLab\DataSet"
    else:
        base_path = r"D:\Code\Python\CrimeLab\TestSet"
    for root, dirs, files in tqdm(os.walk(base_path), desc="处理数据集"):
        for file in files:
            if file.endswith(".txt"):
                crime_name = os.path.basename(root)  # 获取罪名
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    try:
                        # 尝试将数据添加到列表中
                        data.append([crime_name, content])
                    except Exception as e:
                        # 如果出错，记录文件路径并打印异常信息
                        files_skipped.append(file_path)

    # 创建DataFrame
    df = pd.DataFrame(data, columns=["label", "content"])
    # 将数据写入Excel文件
    try:
        with pd.ExcelWriter(xlsx_data_file_path) as writer:
            df.to_excel(writer, sheet_name="CrimesTable", index=False)
        print("CrimesTable.xlsx 已成功生成！")
    except Exception as e:
        if files_skipped:
            print("Files skipped due to error:")
            for file_path in files_skipped:
                print(file_path)
    et = time.time()
    print("生成 .xlsx 文件 耗时: {:.3f}s".format(et - st))


def reset_CrimesDataSet(xlsx_CrimeDataSet_file_path):
    # 创建一个空的DataFrame来存储提取后的数据
    labeled_cases = pd.DataFrame(columns=["content", "label"])
    # 遍历每一行数据
    for index, row in tqdm(df.iterrows()):
        content = row["content"]
        labels = []
        # 遍历所有罪名
        for crime in Crimes:
            # 检查刑事案件内容是否包含罪名
            if isinstance(content, str) and crime in content:
                labels.append(crime)  # 处理数据

        # 将提取的标签添加到数据集中
        if labels:
            for label in labels:
                labeled_cases = pd.concat(
                    [
                        labeled_cases,
                        pd.DataFrame({"content": [content], "label": [label]}),
                    ],
                    ignore_index=True,
                )
    # 保存数据集
    labeled_cases.to_excel(xlsx_CrimeDataSet_file_path, index=False)


def add_xlsx_moneys(xlsx_CrimeDataSet_file_path):
    # 读取Excel文件
    df = pd.read_excel(xlsx_CrimeDataSet_file_path)

    if "moneys" in df.columns:
        print("moneys 已存在 !")
        return
    else:
        df["moneys"] = 0
    output_file_path = xlsx_CrimeDataSet_file_path
    df.to_excel(output_file_path, index=False)

    print(
        f"New column 'moneys' has been added. The file has been saved to '{output_file_path}'."
    )

    df = pd.read_excel(xlsx_CrimeDataSet_file_path, dtype=str)

    df["moneys"] = "-1"

    # 遍历所有罚金
    for money in Moneys:
        # 查找包含罚金的行
        mask = df["content"].str.contains(money, na=False)
        # 将这些行的标签设置为相应的罚金
        df.loc[mask, "moneys"] = money

    # 将标签为 -1 的行删除
    df = df[df["moneys"] != "-1"]
    df.to_excel(xlsx_CrimeDataSet_file_path, index=False)


def add_xlsx_Times(xlsx_CrimeDataSet_file_path):
    # 读取Excel文件
    df = pd.read_excel(xlsx_CrimeDataSet_file_path)

    if "times" in df.columns:
        print("times 已存在 ! ")
        return
    else:
        df["times"] = 0
    output_file_path = xlsx_CrimeDataSet_file_path
    df.to_excel(output_file_path, index=False)

    print(
        f"New column 'times' has been added. The file has been saved to '{output_file_path}'."
    )
    df = pd.read_excel(xlsx_CrimeDataSet_file_path, dtype=str)

    # 将所有标签初始化为 -1
    df["times"] = "-1"

    # 遍历所有刑期
    for sentence in Times:
        # 查找包含刑期的行
        mask = df["content"].str.contains(sentence, na=False)
        # 将这些行的标签设置为相应的刑期
        df.loc[mask, "times"] = sentence

    # 将标签为 -1 的行删除
    df = df[df["times"] != "-1"]

    # 保存数据集
    df.to_excel(xlsx_CrimeDataSet_file_path, index=False)


# 读取金钱列表
Moneys = []
Moneys_folder_path = r"D:\Code\Python\CrimeLab\TestCode\Money.txt"
with open(Moneys_folder_path, "r", encoding="utf-8") as file:
    Moneys = [money.strip() for money in file.readlines()]

Times = []
Times_folder_path = r"D:\Code\Python\CrimeLab\TestCode\Times.txt"
with open(Times_folder_path, "r", encoding="utf-8") as file:
    Times = [time.strip() for time in file.readlines()]


# 读取罪名列表
Begin_time = time.time()


# 遍历子文件夹和文件

if Test == 0:
    xlsx_data_file_path = r"D:\Code\Python\CrimeLab\CrimesTable.xlsx"
else:
    xlsx_data_file_path = r"D:\Code\Python\CrimeLab\TestSet.xlsx"

print(xlsx_data_file_path)

if not os.path.exists(xlsx_data_file_path):
    create_excel_file(xlsx_data_file_path, Test)
    print("CrimesTable.xlsx 已成功生成！")
else:
    print("CrimesTable.xlsx 已存在！")


df = pd.read_excel(xlsx_data_file_path)

if Test == 0:
    xlsx_CrimeDataSet_file_path = r"D:\Code\Python\CrimeLab\CrimesDataSet.xlsx"
else:
    xlsx_CrimeDataSet_file_path = r"D:\Code\Python\CrimeLab\CrimesTestSet.xlsx"

print(xlsx_CrimeDataSet_file_path)

if not os.path.exists(xlsx_CrimeDataSet_file_path):
    st = time.time()
    reset_CrimesDataSet(xlsx_CrimeDataSet_file_path)
    et = time.time()
    print("重置 CrimesDataSet.xlsx 文件 耗时: {:.3f}s".format(et - st))
else:
    print("CrimeDataSet.xlsx 已存在！")

df = pd.read_excel(xlsx_CrimeDataSet_file_path)

df.label.unique()

if TestPrint == 0:
    label_counts = df["label"].value_counts()
    # 打印每个元素的个数
    for label, count in label_counts.items():
        print(f"{label}: {count}")


add_xlsx_moneys(xlsx_CrimeDataSet_file_path)

add_xlsx_Times(xlsx_CrimeDataSet_file_path)

label_dict = {
    "一千元": [
        "",
        "判处拘役二个月",
        "判处拘役三个月",
        "判处拘役四个月",
        "判处拘役五个月",
        "判处拘役六个月",
        "判处拘役七个月",
        "判处拘役八个月",
        "判处拘役九个月",
        "判处拘役十个月",
        "判处拘役十一个月",
        "判处有期徒刑一个月",
        "判处有期徒刑二个月",
        "判处有期徒刑三个月",
        "判处有期徒刑四个月",
        "判处有期徒刑五个月",
        "判处有期徒刑六个月",
        "判处有期徒刑七个月",
        "判处有期徒刑八个月",
        "判处有期徒刑九个月",
        "判处有期徒刑十个月",
        "判处有期徒刑十一个月",
    ],
    "一年": ["判处有期徒刑一年"],
    "-1": ["-1"],
    "免于刑事处罚": ["免予刑事处罚"],
    "死刑": ["判处死刑"],
    "二年": ["判处有期徒刑二年", "判处有期徒刑两年"],
    "三年": ["判处有期徒刑三年"],
    "四年到六年": ["判处有期徒刑四年", "判处有期徒刑五年", "判处有期徒刑六年"],
    "七年到十年": [
        "判处有期徒刑七年",
        "判处有期徒刑八年",
        "判处有期徒刑九年",
        "判处有期徒刑十年",
    ],
    "十年以上": [
        "判处有期徒刑十一年",
        "判处有期徒刑十二年",
        "判处有期徒刑十三年",
        "判处有期徒刑十四年",
        "判处有期徒刑十五年",
        "判处有期徒刑十六年",
        "判处有期徒刑十七年",
        "判处有期徒刑十八年",
        "判处有期徒刑十九年",
        "判处有期徒刑二十年",
        "判处有期徒刑二十一年",
    ],
    "无期": ["判处无期徒刑"],
}


def label_to_category(label):
    for category, labels in label_dict.items():
        if label in labels:
            return category
    return None


df = pd.read_excel(xlsx_CrimeDataSet_file_path)

df["times"] = df["times"].apply(label_to_category)

counts = df.groupby("times").size().reset_index(name="count")

End_time = time.time()
print("生成数据集 耗时: {:.3f}s".format(End_time - Begin_time))
