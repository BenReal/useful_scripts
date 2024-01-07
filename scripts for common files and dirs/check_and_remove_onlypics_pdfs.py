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
from pdfminer.high_level import extract_text


log_file_path = r'../logs/app.log'
configure_logging(log_file_path)
# 记录日志信息
logging.info('程序开始运行')


# 定义扫描文档文件夹路径
scan_folder = r"G:/总备份/图片或扫描文档"

# 判断扫描文档文件夹是否存在，如果不存在则创建
if not os.path.exists(scan_folder):
    os.mkdir(scan_folder)
    print(f"已创建{scan_folder}文件夹")

# 遍历目录及其子目录下的所有pdf文件
for root, dirs, files in os.walk("G:/总备份"):
    for file in files:
        # 判断文件是否为pdf文件
        if file.endswith(".pdf"):
            # 使用pdfminer提取pdf文件中的文本内容
            text = extract_text(os.path.join(root, file))

            # 如果文本内容为空字符串，则将该文件移动到扫描文档文件夹中
            if not text:
                shutil.move(os.path.join(root, file), scan_folder)
                print(f"已将文件{file}移动到{scan_folder}文件夹中")
