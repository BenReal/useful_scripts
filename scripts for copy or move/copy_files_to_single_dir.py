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
from pathlib import Path
import logging
import time
from local_modules.local_functions import configure_logging


def copy_files(source_folder_path, file_list_path, add_file_type, target_folder_name):
    # 读取待复制文件名列表
    with open(file_list_path, "r", encoding="utf8") as f_copy:
        lines_copy = f_copy.readlines()
        file_list = {line.strip() + add_file_type for line in lines_copy if line}

    # 用集合记录已经复制过的文件
    copied_files = set()

    # 使用 Path 遍历目录
    source_folder = Path(source_folder_path)
    target_folder = source_folder / target_folder_name

    # 如果目标文件夹不存在，创建目标文件夹
    target_folder.mkdir(parents=True, exist_ok=True)

    # 遍历目录
    for source_file in source_folder.rglob("*"):
        # 如果是文件且文件名在文件列表中且未被复制过
        if source_file.is_file() and source_file.name in file_list and source_file.name not in copied_files:
            # 目标文件路径
            target_file = target_folder / source_file.name

            try:
                # 复制文件到目标文件夹
                shutil.copy2(source_file, target_file)
                print(f"复制成功：{source_file}")
                logging.info(f"复制成功：{source_file} -> {target_file}")
                # 记录已复制的文件
                copied_files.add(source_file.name)
            except FileNotFoundError:
                print(f"源文件不存在：{source_file}")
                logging.error(f"源文件不存在：{source_file}")
            except Exception as e:
                print(f"复制失败：{source_file}. 错误：{str(e)}")
                logging.error(f"复制失败：{source_file}. 错误：{str(e)}")


if __name__ == "__main__":
    # 获取当前脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_dir_parent = os.path.dirname(script_dir)
    print(script_dir)

    # 设置日志配置
    log_file_path = os.path.join(os.path.dirname(script_dir_parent), '/logs/file_copy_log.log')
    configure_logging(log_file_path)

    # 文件夹路径
    source_folder_path = r"H:\测试"
    add_file_type = '.pdf'
    # add_file_type = '.txt'
    target_folder_name = "待转移"

    # 待复制文件名列表路径
    file_list_path = os.path.join(script_dir_parent, "config", "files_for_move.txt")
    print(script_dir)
    print(file_list_path)
    print()

    # 复制文件
    copy_files(source_folder_path, file_list_path, add_file_type, target_folder_name)

