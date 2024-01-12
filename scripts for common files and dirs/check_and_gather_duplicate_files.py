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
import hashlib
import logging
import time
from local_modules.local_functions import configure_logging
from local_modules.local_functions import calculate_sha256

log_file_path = r'../logs/app.log'
configure_logging(log_file_path)
# 记录日志信息
logging.info('程序开始运行')


# 定义源文件夹和目标文件夹
src_dir = r"H:\竞争连续体2023年11月17日A"
dst_dir = os.path.join(src_dir, '重复文件')

# 如果目标文件夹不存在，则创建它
if not os.path.exists(dst_dir):
    os.makedirs(dst_dir)

# 定义一个字典，用于存储文件内容哈希值和文件路径的对应关系
file_dict = {}

# 定义一个列表，用于存储重复的文件路径
duplicate_files = []

# 遍历源文件夹中的所有文件
for root, dirs, files in os.walk(src_dir):
    for file in files:
        file_path = os.path.join(root, file)

        # 计算文件的哈希值
        with open(file_path, 'rb') as f:
            file_content = f.read()
            file_hash = calculate_sha256(file_content)

        # 如果哈希值已经存在于字典中，则说明当前文件内容与之前的某个文件内容相同，将其加入重复文件列表中
        if file_hash in file_dict:
            duplicate_files.append((file_path, file_dict[file_hash]))
        else:
            file_dict[file_hash] = file_path

# 将重复文件移动到目标文件夹中
i = 1
for file_pair in duplicate_files:
    i += 1
    try:
        print(f"文件'{file_pair[0]}'与文件'{file_pair[1]}'内容重复，移动到目标文件夹中")
        shutil.move(file_pair[0], os.path.join(
            dst_dir, os.path.basename(file_pair[0])))
        shutil.move(file_pair[1], os.path.join(
            dst_dir, os.path.basename(file_pair[1])))
    except:
        continue

    if i > 6:
        break

print("查找重复文件完成")
