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
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from local_modules.local_functions import configure_logging
from local_modules.local_functions import add_timestamp
import pandas as pd
import logging
import time
import re

log_file_path = r'../logs/count_phrases_occarences_in_txts_in_given_dir.log'
configure_logging(log_file_path)

start_time = time.time()
logging.info('Run Time Start up')

directory = r"F:\总备份\文献库"

with open("./useful_scripts/config/phrases_for_search.txt", "r", encoding="utf8") as f_phrases:
    lines_old = f_phrases.readlines()
    phrases = [line.strip() for line in lines_old if line]
    print(phrases)

patterns = [re.compile(phrase, re.IGNORECASE) for phrase in phrases]
filetype = '.txt'


def count_phrases_in_file(filepath, patterns):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    counts = [len(pattern.findall(content)) for pattern in patterns]
    filename = os.path.basename(filepath)
    filename = filename[:-4]
    row = [filename] + counts
    return pd.DataFrame([row], columns=['Filename'] + phrases)


def process_file(root, file):
    try:
        filepath = os.path.join(root, file)
        result = count_phrases_in_file(filepath, patterns)
        print(f"当前文件：{file}")
        return result
    except Exception as e:
        print(f"文件存在未知问题：{file}")
        print(f"错误信息：{e}")
        return None


def count_phrases_in_directory(directory):
    results = pd.DataFrame(columns=['Filename'] + phrases)
    with ThreadPoolExecutor() as executor:
        futures = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(filetype):
                    file_count = len(futures) + 1
                    print(f"进度：{file_count}/{len(files)}")
                    futures.append(executor.submit(partial(process_file, root, file)))

        for future in futures:
            result = future.result()
            if result is not None:
                results = pd.concat([results, result], ignore_index=True)

    return results


results = count_phrases_in_directory(directory)


excel_file_name = "result.xlsx"
excel_file_name = add_timestamp(excel_file_name)
dir_excel_file_name = os.path.join(directory, excel_file_name)

results.to_excel(dir_excel_file_name, index=False)

end_time = time.time()
run_time = end_time - start_time
print("程序运行时间：{}秒".format(run_time))

logging.info('Run Time is over')
logging.info("Total running time: {} seconds".format(run_time))




