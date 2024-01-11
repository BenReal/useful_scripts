import os
import sys
# 获取当前脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
# 如果当前目录是 'useful_scripts'，将当前目录加入搜索路径，否则，将父目录加入搜索路径
if os.path.basename(script_dir) == 'useful_scripts':
    sys.path.append(script_dir)
else:
    parent_dir = os.path.dirname(script_dir)
    sys.path.append(parent_dir)
# 导入其他模块
import pandas as pd
import shutil
import fitz
from local_modules.local_functions import add_timestamp


def count_pdf_pages(folder_path):
    output_folder = os.path.join(folder_path, "pdf页数统计失败文件")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    file_paths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".pdf"):
                file_paths.append(os.path.join(root, file))

    total_files = len(file_paths)
    processed_files = 0

    data = []
    for file_path in file_paths:
        try:
            pdf = fitz.open(file_path)
            num_pages = len(pdf)
            file_size = os.path.getsize(file_path)
            data.append(
                {"File": file_path, "Pages": num_pages, "Size": file_size})
            print(
                f"处理进度: {processed_files}/{total_files} 文件: {file_path} 页数: {num_pages} 大小: {file_size}字节")
        except Exception as e:
            print(f"处理进度: {processed_files}/{total_files} 无法读取文件: {file_path}")
            output_path = os.path.join(
                output_folder, os.path.basename(file_path))
            shutil.move(file_path, output_path)

        processed_files += 1

    df = pd.DataFrame(data)
    return df


folder_path = r"F:\总备份"
result_df = count_pdf_pages(folder_path)


output_file = os.path.join(folder_path, "pdf页数统计.xlsx")
output_file = add_timestamp(output_file)
result_df.to_excel(output_file, index=False)


# 请确保你已经安装了pandas和PyMuPDF库，你可以使用pip命令进行安装：
# pip install pandas PyMuPDF


