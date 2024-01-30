# -*- coding: UTF-8 -*-
import os
import sys
from pathlib import Path
import pandas as pd
import logging
import time
import re
from multiprocessing import Pool, Manager
from functools import partial
# # 获取当前脚本所在目录
# script_dir = Path(__file__).resolve().parent
# # 将当前目录或父目录加入搜索路径
# sys.path.append(script_dir) if script_dir.name == 'useful_scripts' else sys.path.append(script_dir.parent)
# 获取当前脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
# 如果当前目录是 'useful_scripts'，将当前目录加入搜索路径，否则，将父目录加入搜索路径
if os.path.basename(script_dir) == 'useful_scripts':
    sys.path.append(script_dir)
else:
    parent_dir = os.path.dirname(script_dir)
    sys.path.append(parent_dir)
# 导入其他模块
from local_modules.local_functions import configure_logging, add_timestamp


# 装饰器：记录函数运行时间
def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        logging.info(f"{func.__name__} - Total time taken: {elapsed_time:.2f} seconds")
        return result
    return wrapper


# 读取短语列表
def read_phrases(phrases_file_path):
    with phrases_file_path.open("r", encoding="utf8") as f_phrases:
        return [line.strip() for line in f_phrases if line]

# 编译正则表达式
def compile_patterns(phrases):
    return [re.compile(phrase, re.IGNORECASE) for phrase in phrases]

# 统计单个文件中短语出现的次数
def count_phrases_in_file(filepath, patterns, phrases):
    with filepath.open('r', encoding='utf-8') as f:
        content = f.read()

    counts = [len(pattern.findall(content)) for pattern in patterns]
    filename = filepath.stem
    return {'Filename': filename, **dict(zip(phrases, counts))}


def count_phrases_in_file_partial(file_path, patterns, phrases, result_dicts, num_files):
    try:
        result_dict = count_phrases_in_file(file_path, patterns, phrases)
        result_dicts.append(result_dict)
        print(f"进度：{len(result_dicts)}/{num_files}，当前文件：{file_path.name}")
    except Exception as e:
        print(f"文件存在未知问题：{file_path.name} - {str(e)}")


# 统计目录中所有txt文件中短语出现的次数
def count_phrases_in_directory_parallel(directory, patterns, phrases, file_type):
    num_files = sum(1 for _ in directory.rglob(f"*{file_type}"))
    result_dicts = Manager().list()

    # 使用多进程 Pool 处理
    with Pool() as pool:
        partial_count_phrases_in_file = partial(count_phrases_in_file_partial, patterns=patterns, phrases=phrases, result_dicts=result_dicts, num_files=num_files)
        pool.map(partial_count_phrases_in_file, directory.rglob(f"*{file_type}"))

    results = pd.DataFrame(list(result_dicts))

    return results


# 装饰器应用：记录函数运行时间
@timing_decorator
def main():
    script_dir = Path(__file__).resolve().parent
    phrases_file_path = Path(script_dir.parent / "config" / "phrases_for_search.txt")
    # 要搜索的目录
    directory = Path("F:\总备份\文献库")
    file_type = '.txt'
    phrases = read_phrases(phrases_file_path)
    patterns = compile_patterns(phrases)
    results = count_phrases_in_directory_parallel(directory, patterns, phrases, file_type)

    # 保存到Excel文件
    excel_file_name = "腾云无人机词频统计.xlsx"
    excel_file_name = add_timestamp(excel_file_name)
    excel_path = directory / excel_file_name
    results.to_excel(excel_path, index=False)


if __name__ == "__main__":
    # 配置日志
    log_file_path = '../logs/count_phrases_occarences_in_txts_in_given_dir.log'
    configure_logging(log_file_path)
    main()
