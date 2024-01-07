# -*- coding: utf-8 -*-
import os
import sys


def check_files_in_folder(file_list_path, folder_path):
    # 读取文件名称列表
    with open(file_list_path, 'r') as file:
        file_names = file.read().splitlines()

    # 获取文件夹中的文件列表
    folder_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            folder_files.append(file)

    # 检查文件名称列表中的文件是否存在于文件夹中
    missing_files = []
    for file_name in file_names:
        if file_name not in folder_files:
            missing_files.append(file_name)

    return missing_files


def main(file_list_path, folder_path):
    # 调用函数检查文件名称列表中的文件是否存在于文件夹中
    missing_files = check_files_in_folder(file_list_path, folder_path)

    # 输出缺失的文件
    print("缺失的文件:")
    for file_name in missing_files:
        print(file_name)


if __name__ == '__main__':
    # # 检查命令行参数数量
    # if len(sys.argv) != 3:
    #     print("请提供正确的命令行参数：文件名称列表路径 和 文件夹路径")
    #     sys.exit(1)

    # # 提取命令行参数
    # file_list_path = sys.argv[1]
    # folder_path = sys.argv[2]

    file_list_path = r'./config/filenames_missing_for_check.txt'
    folder_path = r'D:'


    # 调用主函数
    main(file_list_path, folder_path)


