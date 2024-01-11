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
import PyPDF2
from pathlib import Path
from local_modules.local_functions import add_timestamp
from local_modules.pdf_functions import read_pdf_metadata


# def generate_row_data(folder_path):
#     """
#     Generate row data by traversing the folder directory tree.

#     Args:
#         folder_path (str): The path to the folder.

#     Yields:
#         dict: Row data for each file.
#     """
#     folder_path = Path(folder_path).resolve()
#     for file_path in folder_path.glob('**/*.pdf'):
#         metadata = read_pdf_metadata(str(file_path))
#         row = {'文件名': file_path.name}
#         row.update(metadata)
#         yield row

# # 生成器函数生成行数据
# def generate_row_data(folder_path):
#     folder_path = Path(folder_path).resolve()
#     for file_path in folder_path.glob('**/*'):
#         if file_path.suffix.lower() == '.pdf':
#             metadata = read_pdf_metadata(str(file_path))
#             row = {'文件名': file_path.name}
#             row.update(metadata)
#             yield row


def generate_row_data(folder_path):
    """
    Generate row data by traversing the folder directory tree.

    Args:
        folder_path (str): The path to the folder.

    Yields:
        dict: Row data for each file.
    """
    folder_path = Path(folder_path).resolve()
    pdf_files = list(folder_path.glob("**/*.[pP][dD][fF]"))
    total_files = len(pdf_files)
    processed_files = 0

    for file_path in pdf_files:
        processed_files += 1
        # 打印处理进度信息
        print(f"进度: {processed_files}/{total_files} : {file_path}")
        metadata = read_pdf_metadata(str(file_path))
        row = {'文件名': file_path.name}
        row.update(metadata)
        yield row

    print("处理完成！")


def export_to_excel(df, output_file):
    """
    Export DataFrame to Excel file.

    Args:
        df (pandas.DataFrame): The DataFrame to export.
        output_file (str): The path to the output Excel file.
    """
    df.to_excel(output_file, index=False)

def main():
    # 设置文件夹路径
    folder_path = r'F:\总备份'

    # 生成器函数生成行数据
    row_data = generate_row_data(folder_path)

    # 将所有行数据一次性合并为一个数据帧
    df = pd.DataFrame(row_data)

    # 导出DataFrame为Excel文件
    output_file = os.path.join(folder_path,r'pdf_metadata1.xlsx')
    output_file = add_timestamp(output_file)
    export_to_excel(df, output_file)

if __name__ == '__main__':
    main()



# import os
# import pandas as pd
# import PyPDF2

# def read_pdf_metadata(pdf_path):
#     """
#     Read metadata information from a PDF file.

#     Args:
#         pdf_path (str): The path to the PDF file.

#     Returns:
#         dict: Metadata information.
#     """
#     with open(pdf_path, 'rb') as pdf_file:
#         pdf_reader = PyPDF2.PdfReader(pdf_file)
#         metadata = pdf_reader.metadata
#         return metadata

# # 设置文件夹路径
# folder_path = r'H:\测试'

# # 创建空的DataFrame
# df = pd.DataFrame()  # 不再预定义列名

# # # 遍历文件夹目录树
# # for root, dirs, files in os.walk(folder_path):
# #     for file in files:
# #         if file.endswith('.pdf'):
# #             # 构建PDF文件的完整路径
# #             pdf_path = os.path.join(root, file)
# #             # 读取PDF文件的元数据
# #             metadata = read_pdf_metadata(pdf_path)
# #             print(metadata)
# #             # 将文件名和元数据的键值对添加到DataFrame中
# #             row = {'文件名': file}
# #             row.update(metadata)  # 直接将元数据字典添加到行字典中
# #             df = pd.concat([df, pd.DataFrame(row, index=[0])], ignore_index=True)


# # 在上述代码中，每次迭代时，pd.DataFrame(row, index=[0])会创建一个临时的数据帧来表示当前行的数据。然后，pd.concat()函数将这个临时的数据帧与原始的df数据帧进行合并。
# # 尽管这种方法可以实现将行数据追加到DataFrame中，但对于大型数据集或大量迭代的情况，可能会导致性能下降。
# # 如果处理的数据集非常大，或者有大量的行数据需要添加到DataFrame中，建议考虑其他更高效的方法，比如先将行数据存储在列表中，然后一次性使用pd.concat()函数将它们合并为一个数据帧。

# # 创建空的列表来存储行数据
# row_data = []

# # 遍历文件夹目录树
# for root, dirs, files in os.walk(folder_path):
#     for file in files:
#         if file.endswith('.pdf'):
#             # 构建PDF文件的完整路径
#             pdf_path = os.path.join(root, file)
#             # 读取PDF文件的元数据
#             metadata = read_pdf_metadata(pdf_path)
#             # 将文件名和元数据的键值对添加到列表中
#             row = {'文件名': file}
#             row.update(metadata)  # 直接将元数据字典添加到行字典中
#             row_data.append(row)

# # 将所有行数据一次性合并为一个数据帧
# df = pd.concat([df, pd.DataFrame(row_data)], ignore_index=True)

# # 导出DataFrame为Excel文件
# output_file = r'H:\测试\pdf_metadata1.xlsx'
# df.to_excel(output_file, index=False)

