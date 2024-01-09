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
import pandas as pd
import logging
import time
from local_modules.local_functions import configure_logging

log_file_path = r'../logs/move_dirs_to_different_parent_dir.log'
configure_logging(log_file_path)


def move_folders(df, root_folder):
    for index, row in df.iterrows():
        folder_name = str(row[0])
        target_folder_name = str(row[1])

        # 构造源文件夹的完整路径
        source_folder_path = os.path.join(root_folder, folder_name)

        # 构造目标文件夹的完整路径
        target_folder_path = os.path.join(root_folder, target_folder_name)

        # 构造源文件夹移动之后的最终路径
        folder_name_target_path = os.path.join(target_folder_path, folder_name)

        # 如果目标文件夹不存在，则创建
        if not os.path.exists(target_folder_path):
            os.makedirs(target_folder_path, exist_ok=True)
            logging.info(f"Created target folder: {target_folder_path}")

        if os.path.exists(folder_name_target_path):
            logging.warning(f"Destination folder already exists: {folder_name_target_path}. Choose a different destination.")
        else:
            try:
                # 移动文件夹
                shutil.move(source_folder_path, target_folder_path)
                logging.info(f"Moved folder: {source_folder_path} -> {target_folder_path}")
            except Exception as e:
                logging.error(f"Failed to move folder: {source_folder_path} -> {target_folder_path}. Error: {str(e)}")

def main():
    # 读取Excel文件
    df = pd.read_excel("./useful_scripts/config/move_folder.xlsx")

    # 指定根文件夹路径
    root_folder = "path/to/root_folder"

    # 检查数据框是否为空
    if df.empty:
        logging.info("DataFrame is empty. No folders to move.")
    else:
        # 记录程序开始时间
        start_time = time.time()

        move_folders(df, root_folder)

        # 记录程序结束时间并计算运行时长
        end_time = time.time()
        run_time = end_time - start_time
        logging.info("程序运行时间：{}秒".format(run_time))

if __name__ == '__main__':
    main()


# 请写一个Python脚本实现下面功能：
# 1、有一个根文件夹，包含子文件夹，每个子文件夹需要移动到新的位置；
# 2、需要移动的文件夹名信息保存在一个Excel文件夹中，名为"move_file.xlsx"，其第一列表示文件夹名，第二列为要移动到的文件夹的名字（要移动到的文件夹都是根文件夹的直接子文件夹，如果不存在，需要创建）。
# 3、注意，要移动的是文件夹，不是文件。


