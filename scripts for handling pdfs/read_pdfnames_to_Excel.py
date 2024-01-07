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
import pandas as pd

log_file_path = r'../logs/app.log'
configure_logging(log_file_path)
# 记录日志信息
logging.info('程序开始运行')

# 指定文件夹路径
folder_path = "G:\资料检索"

# 获取子文件夹列表
subfolders = [f.path for f in os.scandir(folder_path) if f.is_dir()]

# 遍历子文件夹
for subfolder in subfolders:
    # 获取子文件夹名称
    folder_name = os.path.basename(subfolder)

    # 获取子文件夹中的pdf文件列表并按名称排序
    pdf_files = sorted([f for f in os.listdir(subfolder) if f.endswith(".pdf")])

    if pdf_files:
        # 创建一个空的DataFrame，包括"文件名"和"年份"两列
        df = pd.DataFrame({'文件名': pdf_files, '年份': [None] * len(pdf_files)})

        # 保存DataFrame到Excel文件
        excel_file_path = os.path.join(folder_path, f"{folder_name}.xlsx")
        df.to_excel(excel_file_path, index=False)

        print(f"Created {excel_file_path}")

logging.info('程序运行结束')

