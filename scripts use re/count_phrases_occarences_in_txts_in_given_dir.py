# -*- coding: UTF-8 -*-
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
import re
import pandas as pd

log_file_path = r'../logs/count_phrases_occarences_in_txts_in_given_dir.log'
configure_logging(log_file_path)

start_time = time.time()
# 记录日志信息

logging.info('Run Time Start up')


directory = r"G:\资料检索\新建文件夹"
# 定义要搜索的短语列表
with open("./config/phrases_for_search.txt", "r", encoding="utf8") as f_phrases:
    lines_old = f_phrases.readlines()
    phrases = [line.strip() for line in lines_old if line]
    print(phrases)


# 定义正则表达式，用于匹配单词并不区分大小写
patterns = [re.compile(phrase, re.IGNORECASE) for phrase in phrases]

# 定义要搜索的文件类型
filetype = '.txt'

# 定义函数，用于统计单个文件中短语出现的次数
def count_phrases_in_file(filepath):
    # 读取文件内容
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # # 临时使用（2023年11月9日）：截取文本前后两部分
    # if len(content) > 310:
    #     content = content[:300]
    # # print(len(content))


    # 统计短语出现的次数
    counts = [len(pattern.findall(content)) for pattern in patterns]
    # 将文件名和统计结果组成一行DataFrame
    filename = os.path.basename(filepath)
    filename = filename[:-4]
    row = [filename] + counts
    return pd.DataFrame([row], columns=['Filename'] + phrases)

# 定义函数，用于遍历目录并统计所有txt文件中短语出现的次数
def count_phrases_in_directory(directory):
    num_files = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(filetype):
                num_files += 1

    file_count = 0

    # 定义保存结果的DataFrame
    results = pd.DataFrame(columns=['Filename'] + phrases)
    # 遍历目录
    for root, dirs, files in os.walk(directory):
        for file in files:
            # 如果文件类型符合要求，则统计短语出现的次数并保存到结果DataFrame中
            if file.lower().endswith(filetype):
                try:
                    file_count += 1
                    filepath = os.path.join(root, file)
                    result = count_phrases_in_file(filepath)
                    results = pd.concat([results, result], ignore_index=True)
                    # 打印统计结果
                    print(f"进度：{file_count}/{num_files}，当前文件：{file}")
                    # print(result)
                except:
                    print(f"文件存在未知问题：{file}")
                    continue
    # 返回结果DataFrame
    return results

# 统计指定目录下所有txt文件中短语出现的次数，并保存到Excel文件中


results = count_phrases_in_directory(directory)

current_time = time.time()  # 获取当前时间的时间戳
current_time_tuple = time.localtime(current_time)  # 将时间戳转换为本地时间的struct_time元组
current_time_str = time.strftime(
    "%Y-%m-%d %H:%M:%S", current_time_tuple)  # 将struct_time元组转换为字符串格式
current_time_str = current_time_str.replace(':', '').replace(' ', '_')

excel_file_name = "result_" + current_time_str + '.xlsx'

dir_excel_file_name = os.path.join(directory, excel_file_name)

results.to_excel(dir_excel_file_name, index=False)


end_time = time.time()
run_time = end_time - start_time
print("程序运行时间：{}秒".format(run_time))
# 记录日志信息
logging.info('Run Time is over')
logging.info("Total running time: {} seconds".format(run_time))
