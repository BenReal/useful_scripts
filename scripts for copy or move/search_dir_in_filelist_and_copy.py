# -*- coding: utf-8 -*-
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
from local_modules.local_functions import configure_logging

# 设置日志配置
log_file_path = r'../logs/file_copy_log.log'
configure_logging(log_file_path)


# 文件夹路径
source_folder_path = r"G:\总备份"

# 复制目标文件夹路径
target_folder_path = os.path.join(source_folder_path, "重点")

# 待复制文件名列表
with open("./useful_scripts/config/files_for_move.txt", "r", encoding="utf8") as f_copy:
    lines_copy = f_copy.readlines()
    file_list = {line.strip() + ".pdf" for line in lines_copy if line}

# 如果目标文件夹不存在，创建目标文件夹
if not os.path.exists(target_folder_path):
    os.makedirs(target_folder_path)

# 用集合记录已经复制过的文件
copied_files = set()

# 遍历目录
for root, dirs, files in os.walk(source_folder_path):
    # 遍历文件
    for file in files:
        # 如果文件名在文件列表中且未被复制过
        if file in file_list and file not in copied_files:
            # 源文件路径
            source_file = os.path.join(root, file)
            # 目标文件路径
            target_file = os.path.join(target_folder_path, file)

            try:
                # 复制文件到目标文件夹
                shutil.copy2(source_file, target_file)
                print(f"复制成功：{source_file}")
                logging.info(f"复制成功：{source_file} -> {target_file}")
                # 记录已复制的文件
                copied_files.add(file)
            except FileNotFoundError:
                print(f"源文件不存在：{source_file}")
                logging.error(f"源文件不存在：{source_file}")
            except Exception as e:
                print(f"复制失败：{source_file}. 错误：{str(e)}")
                logging.error(f"复制失败：{source_file}. 错误：{str(e)}")
