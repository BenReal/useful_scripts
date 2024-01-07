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
import chardet


log_file_path = r'../logs/app.log'
configure_logging(log_file_path)

# # 记录日志信息
# logging.info('程序开始运行')


def convert_encoding_to_utf8(path):
    """
    将指定路径下的文件的编码格式转换成utf-8
    :param path: 文件路径
    """
    # 打开文件并读取内容
    with open(path, 'rb') as f:
        content = f.read()

    # 判断文件的编码格式    
    result = chardet.detect(content)
    encoding = result['encoding']

    # 如果chardet无法检测编码格式，则使用默认编码格式
    if encoding is None:
        encoding = 'utf-8'

    # 如果文件的编码格式不是utf-8，则将其转换成utf-8编码
    if encoding.lower() != 'utf-8':
        with open(path, 'w', encoding='utf-8', errors='replace') as f:
            f.write(content.decode(encoding, errors='replace'))

def count_all_txts(path):
    """
    统计指定路径下的所有txt文件的数量
    :param path: 文件路径
    """
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if os.path.splitext(file)[1].lower() in ['.txt', '.log']:
                count += 1
    return count

def convert_all_txts_to_utf8(path):
    """
    将指定路径下的所有txt文件的编码格式转换成utf-8
    :param path: 文件路径
    """
    # 统计txt文件总数
    total_count = count_all_txts(path)

    # 初始化计数器
    count = 0

    # 遍历路径下的所有文件和子文件夹
    for root, dirs, files in os.walk(path):
        for file in files:
            # 获取文件路径
            file_path = os.path.join(root, file)

            # 如果文件扩展名为txt，则将其编码格式转换成utf-8
            if os.path.splitext(file_path)[1].lower() in ['.txt', '.log']:
                convert_encoding_to_utf8(file_path)

                # 计数器加1并打印进度信息
                count += 1
                print(f'Converted {count}/{total_count} files')


if __name__ == '__main__':

    # 指定文件夹路径
    folder_path = r"./log"

    # 将所有txt文件的编码格式转换成utf-8
    convert_all_txts_to_utf8(folder_path)
