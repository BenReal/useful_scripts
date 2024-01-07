import os
import pandas as pd
import shutil
import fitz


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


folder_path = r"H:\《XXXX》《XXXX》2023年10月27日\数据库补充资料\科研机构（分拆）\转换完成"
result_df = count_pdf_pages(folder_path)


output_file = os.path.join(folder_path, "pdf文档页数统计.xlsx")
result_df.to_excel(output_file, index=False)


# 请确保你已经安装了pandas和PyMuPDF库，你可以使用pip命令进行安装：
# pip install pandas PyMuPDF


