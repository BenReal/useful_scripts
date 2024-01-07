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


# 配置日志文件
log_file_path = r'../logs/move_files_to_same_dir.log'
configure_logging(log_file_path)

def move_files_to_single_subdir(source_folder_path, target_folder_path, file_list):
    # 遍历目录
    for root, dirs, files in os.walk(source_folder_path):
        if root == target_folder_path:
            continue
        
        # 遍历文件
        for file in files:
            # 如果文件名在文件列表中
            for filename in file_list:
                if filename == file.lower():
                # if filename in file:
                    # 源文件路径
                    source_file = os.path.join(root, filename)
                    # 目标文件路径
                    target_file = os.path.join(target_folder_path, filename)

                    try:
                        shutil.move(source_file, target_file)
                    except:
                        # 如果目标文件已经存在，添加数字后缀
                        i = 1
                        while os.path.exists(target_file):
                            target_file = os.path.join(
                                target_folder_path, f"{os.path.splitext(file)[0]}_{i}{os.path.splitext(file)[1]}")
                            i += 1
                        try:
                            # 复制文件到目标文件夹
                            shutil.copy2(source_file, target_file)
                            # 删除源文件
                            os.remove(source_file)
                        except:
                            print(f"移动失败：{source_file}")
                            continue
                        continue


if __name__ == '__main__':
    # 文件夹路径
    # source_folder_path_list = [r"H:\无人机分布式自主蜂群+反无人机蜂群2023年11月29日2023年11月29日", ]
    source_folder_path_list = [r"F:\总备份\文献库", ]

    # 移动目标子文件夹名称
    target_folder = r'待删除'

    # 文件名称是否添加扩展名标识符
    extension_add_symbol = 0 #不用添加扩展名
    # extension_add_symbol = 1 # 添加txt
    # extension_add_symbol = 2 # 添加pdf
    # extension_add_symbol = 3 # 添加txt和pdf

    
    with open("./config/files_for_move.txt", "r", encoding="utf8") as f_move:    
        file_lines = f_move.readlines()
        for source_folder_path in source_folder_path_list:
            if extension_add_symbol == 0:
                file_list = [line.strip().lower() for line in file_lines if line]

            if extension_add_symbol == 1:
                file_list = [line.strip().lower() + ".txt" for line in file_lines if line]

            if extension_add_symbol == 2:
                file_list = [line.strip().lower() + ".pdf" for line in file_lines if line]
            
            if extension_add_symbol == 3:
                file_list_txt = [line.strip().lower() + ".txt" for line in file_lines if line] 
                file_list_pdf = [line.strip().lower() + ".pdf" for line in file_lines if line]
                file_list = file_list_txt + file_list_pdf

            print(file_list)

            # 移动目标文件夹路径            
            target_folder_path = os.path.join(source_folder_path, target_folder)

            # 如果目标文件夹不存在，创建目标文件夹
            if not os.path.exists(target_folder_path):
                os.makedirs(target_folder_path)

            move_files_to_single_subdir(source_folder_path, target_folder_path, file_list)


