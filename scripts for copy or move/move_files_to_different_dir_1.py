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
import shutil
import logging
import time
import pandas as pd
from local_modules.local_functions import configure_logging


# 配置日志文件
log_file_path = r'../logs/move_files_to_different_dir.log'
configure_logging(log_file_path)


def move_files(df, root_folder):
    for index, row in df.iterrows():
        file_name = row[0]
        target_folder_name = row[1]

        # 构造源文件的完整路径
        source_filepath = os.path.join(root_folder, file_name)

        # 构造目标文件夹的完整路径
        target_folder_path = os.path.join(root_folder, target_folder_name)

        # 如果目标文件夹不存在，则创建
        if not os.path.exists(target_folder_path):
            os.makedirs(target_folder_path)
            logging.info(f"Created target folder: {target_folder_path}")

        # 构造目标文件的完整路径
        target_filepath = os.path.join(target_folder_path, file_name)

        if os.path.exists(target_filepath):
            logging.warning(f"Destination file already exists: {target_filepath}. Choose a different destination.")
        else:
            try:
                # 复制文件
                shutil.move(source_filepath, target_filepath)
                logging.info(f"Moved file: {source_filepath} -> {target_filepath}")
            except Exception as e:
                logging.error(f"Failed to move file: {source_filepath} -> {target_filepath}. Error: {str(e)}")

def main():
    # 读取Excel文件
    df = pd.read_excel("./config/move_file.xlsx")

    # 指定根文件夹路径
    root_folder = "H:\《XXXX》《XXXX》2023年10月27日\数据库补充资料\科研机构（分拆）\转换完成"

    # 检查数据框是否为空
    if df.empty:
        logging.info("DataFrame is empty. No files to move.")
    else:
        move_files(df, root_folder)

if __name__ == '__main__':
    main()


# Python脚本实现下面功能：
# 1、有一个根文件夹，包含多层子文件夹，每个子文件夹中都可能包含一些文件夹，文件夹中有很多文件需要复制到新的位置；
# 2、需要复制文件夹的文件名信息保存在一个Excel文件夹中，名为"move_file.xlsx"，其第一列表示文件名（只有文件名，不包含完整路径），第二列为要复制到的文件夹的名字（要复制到的文件夹都是根文件夹的直接子文件夹，如果不存在，需要创建）。

