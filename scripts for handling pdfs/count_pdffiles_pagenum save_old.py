import os
import pandas as pd
from PyPDF2 import PdfFileReader
import shutil


def count_pdf_pages(folder_path):
    output_folder = os.path.join(folder_path, "pdf页数统计失败文件")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    file_paths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".pdf"):
                file_paths.append(os.path.join(root, file))

    total_files = len(file_paths)
    processed_files = 0

    data = []
    for file_path in file_paths:
        try:
            with open(file_path, "rb") as f:
                pdf = PdfFileReader(f)
                num_pages = pdf.getNumPages()
                data.append({"File": file_path, "Pages": num_pages})
                print(
                    f"处理进度: {processed_files}/{total_files} 文件: {file_path} 页数: {num_pages}")
        except Exception as e:
            print(f"处理进度: {processed_files}/{total_files} 无法读取文件: {file_path}")
            output_path = os.path.join(
                output_folder, os.path.basename(file_path))
            shutil.move(file_path, output_path)

        processed_files += 1

    df = pd.DataFrame(data)
    return df


folder_path = r"D:\数据库项目\待整理文件（需要重命名）"
result_df = count_pdf_pages(folder_path)


output_file = os.path.join(folder_path, "pdf文档页数统计.xlsx")
result_df.to_excel(output_file, index=False)
