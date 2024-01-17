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
import pandas as pd
import logging
import time
from local_modules.local_functions import configure_logging

# Constants
LOG_FILE_PATH = r'../logs/rename_files_in_givendir.log'
CONFIG_PATH = "./config"
EXCEL_FILE_NAME = "rename.xlsx"

configure_logging(LOG_FILE_PATH)


def get_new_filename(filename, sequence):
    base, ext = os.path.splitext(filename)
    return f"{base}_{sequence}{ext}"

def find_available_excel_file_path(directory_path, excel_file_name):
    sequence = 1
    new_excel_file_name = get_new_filename(excel_file_name, sequence)
    new_excel_file_path = os.path.join(directory_path, new_excel_file_name)

    while os.path.exists(new_excel_file_path):
        sequence += 1
        new_excel_file_name = get_new_filename(excel_file_name, sequence)
        new_excel_file_path = os.path.join(directory_path, new_excel_file_name)

    return new_excel_file_path

def rename_files(root_folder, df):
    success_count = 0
    failure_count = 0

    for index, row in df.iterrows():
        old_filename = row[0]
        new_filename = row[1]

        for root, dirs, files in os.walk(root_folder):
            for file in files:
                if file.lower() == old_filename.lower():
                    old_filepath = os.path.join(root, file)
                    new_filepath = os.path.join(root, new_filename)

                    try:
                        os.rename(old_filepath, new_filepath)
                        success_count += 1
                        logging.info(f"Renamed file: {old_filepath} -> {new_filepath}")
                    except Exception as e:
                        failure_count += 1
                        logging.error(f"Failed to rename file: {old_filepath} -> {new_filepath}. Error: {str(e)}")

    print(f"Renamed {success_count} files successfully.")
    print(f"Failed to rename {failure_count} files. Check the log file for details.")

if __name__ == "__main__":
    start_time = time.time()

    # Ensure log file exists and is properly configured
    log_file_path = r'../logs/rename_files_in_givendir.log'
    with open(log_file_path, 'a', encoding='utf8') as log_file:
        configure_logging(log_file_path)

    # Log start time
    logging.info('Run Time Start up')

    # Read Excel file
    df = pd.read_excel(os.path.join(CONFIG_PATH, EXCEL_FILE_NAME))

    # Specify root folder
    root_folder = r"G:\资料检索\新建文件夹\台湾相关文献"

    # Rename files
    rename_files(root_folder, df)

    # # Find a new name for the Excel file if it already exists
    # excel_file_path = os.path.join(CONFIG_PATH, EXCEL_FILE_NAME)
    # if os.path.exists(excel_file_path):
    #     new_excel_file_path = find_available_excel_file_path(CONFIG_PATH, EXCEL_FILE_NAME)
    #     os.rename(excel_file_path, new_excel_file_path)
    #     print(f"Renamed Excel file: {excel_file_path} -> {new_excel_file_path}")
    # else:
    #     print("Excel file does not exist in the specified directory.")

    end_time = time.time()
    run_time = end_time - start_time
    print(f"程序运行时间：{run_time}秒")

    # Log end time
    logging.info('Run Time is over')
    logging.info("Total running time: {} seconds".format(run_time))


