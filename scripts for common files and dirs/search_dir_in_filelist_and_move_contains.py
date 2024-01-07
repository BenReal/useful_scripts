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


log_file_path = r'../logs/app.log'
configure_logging(log_file_path)

# 记录日志信息
logging.info('程序开始运行')


# 文件夹路径
source_folder_path = r"H:\新型作战力量、联合作战动态战斗任务规划等研究综述专题报告"

# 移动目标文件夹路径
target_folder_path = os.path.join(source_folder_path, "其他无用")
# 待检查文件名列表


with open("./config/files_for_move.txt", "r", encoding="utf8") as f_move:
    lines_move = f_move.readlines()
    file_list = [line.strip() for line in lines_move if line]
    file_list = [line for line in file_list if line]
    print(file_list)


# 如果目标文件夹不存在，创建目标文件夹
if not os.path.exists(target_folder_path):
    os.makedirs(target_folder_path)

# 遍历目录
for root, dirs, files in os.walk(source_folder_path):
    # 遍历文件
    for file in files:
        # 如果文件名在文件列表中
        for filename in file_list:
            # if filename == file:
            if filename in file.split('/')[-1]:
                # print(filename, file)

                # 源文件路径
                source_file = os.path.join(root, file)
                # 目标文件路径
                target_file = os.path.join(target_folder_path, file)

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
