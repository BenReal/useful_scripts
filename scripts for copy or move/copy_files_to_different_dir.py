import pandas as pd
import os
import shutil

def copy_files_from_excel(excel_path, source_folder, destination_folder):
    # 读取Excel文件
    df = pd.read_excel(excel_path)

    # 遍历每一行
    for index, row in df.iterrows():
        # 获取文件名和目标文件夹信息
        file_name = row['File_Name']
        target_folder_info = row['Target_Folder_Info']

        # 用"【】"分隔目标文件夹信息
        target_folders = target_folder_info.split('【】')

        # 构建目标文件夹路径
        destination_path = os.path.join(destination_folder, *target_folders)

        # 检查目标文件夹是否存在，如果不存在则创建
        os.makedirs(destination_path, exist_ok=True)

        # 构建源文件路径
        source_path = os.path.join(source_folder, file_name)

        # 复制文件到目标文件夹
        shutil.copy(source_path, destination_path)

if __name__ == "__main__":
    # 替换成实际的文件路径和文件夹路径
    excel_path = 'ABC/excel_file.xlsx'
    source_folder = 'ABC/DEF'
    destination_folder = 'XYZ'

    copy_files_from_excel(excel_path, source_folder, destination_folder)


# 某个目录ABC中有一个Excel文件：
# 第一列为文件名，用作每一行ID字段，这些文件名都位于文件夹“DEF”的目录树中。
# 第二列中每一行是一个字符串，可以从中获取目标文件夹的信息，用"【】"将其分隔为多个字符串，每个字符串是目标文件夹的名称。
# 现在第一列中的列出的每个文件复制到文件夹“XYZ”下面的一个或多个文件夹中，具体的文件名名称就是从第二列获取的名称（即用【】分隔开的多个名称）


