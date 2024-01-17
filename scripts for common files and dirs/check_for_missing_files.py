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

    file_list_path = r'./useful_scripts/config/filenames_missing_for_check.txt'
    folder_path = r'D:'


    # 调用主函数
    main(file_list_path, folder_path)


# 这个脚本的主要功能是检查给定文件夹中是否存在文件名称列表中列举的文件。具体而言，它包括以下步骤：

# 从指定的文件路径（file_list_path）读取文件名称列表。
# 获取指定文件夹路径（folder_path）中的所有文件。
# 检查文件名称列表中的每个文件是否存在于文件夹中。
# 输出缺失的文件列表。
# 脚本的主函数 main 调用了 check_files_in_folder 函数，后者执行实际的文件检查操作。在执行时，它会输出文件夹中缺失的文件。

# 此外，脚本中注释掉了一些与命令行参数相关的代码。如果取消注释并提供正确的命令行参数（文件名称列表路径和文件夹路径），则脚本将使用命令行参数进行操作。在当前状态下，它使用了硬编码的路径作为示例。

# 总体而言，这个脚本的目的是帮助用户检查给定文件夹中是否存在指定的文件列表，以确保文件的完整性。
