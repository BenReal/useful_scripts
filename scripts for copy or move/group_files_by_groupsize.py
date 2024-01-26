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


# 指定abc文件夹路径
abc_folder = r"F:\总备份\文献库\中文文献库（pdf+txt）"

# 每组文件的数量
group_size = 3000

# 创建子文件夹的计数器
folder_counter = 1

# 遍历abc文件夹下的所有PDF文件
pdf_files = [file for file in os.listdir(abc_folder) if file.lower().endswith(".pdf")]
pdf_files.sort()

# 按每组文件数量进行分组并存放到子文件夹中
for i in range(0, len(pdf_files), group_size):
    # 创建子文件夹
    subfolder_name = f"文献组_{folder_counter}"
    subfolder_path = os.path.join(abc_folder, subfolder_name)
    os.makedirs(subfolder_path, exist_ok=True)
    
    # 获取当前分组的文件列表
    group_files = pdf_files[i:i+group_size]
    
    # 将分组的文件移动到子文件夹中
    for file in group_files:
        source_path = os.path.join(abc_folder, file)
        destination_path = os.path.join(subfolder_path, file)
        shutil.move(source_path, destination_path)
    
    folder_counter += 1
