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


# 指定要遍历的文件夹路径
folder_path = r"G:/中转文件"

def is_chinese_character(char):
    unicode_value = ord(char)
    if 0x4E00 <= unicode_value <= 0x9FFF:
        return True
    else:
        return False

def remove_spaces_after_chinese(text):
    result = ""
    i = 0
    while i < len(text):
        char = text[i]
        if is_chinese_character(char):
            result += char
            i += 1
            while i < len(text) and text[i] == " ":
                i += 1
        else:
            result += char
            i += 1
    return result

def remove_empty_lines(text):
    # 去除空行
    lines = text.split('\n')
    non_empty_lines = [line for line in lines if line.strip() != '']
    return '\n'.join(non_empty_lines)


def convert_txt_to_txt(folder_path):
    num_files = 0
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".txt"):
                num_files += 1

    file_count = 0

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # print(file)
            if file.endswith(".txt"):
                # print(file)
                file_path = os.path.join(root, file)
                txt_file_path = os.path.splitext(file_path)[0] + ".txt"

                text = ''

                with open(txt_file_path, 'r', encoding='utf-8') as txt_file:
                    text = txt_file.read()
                    text = remove_empty_lines(text)
                    text = text.translate(str.maketrans(
                        "０１２３４５６７８９　ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ",
                        "0123456789 ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
                    ))
                    
                    # 删除中文字符后的空格
                    text = remove_spaces_after_chinese(text)  

                with open(txt_file_path, 'w', encoding='utf-8') as txt_file:                  
                    txt_file.write(text)

                file_count += 1
                print(f"转换进度：{file_count}/{num_files}，当前文件：{file}")


convert_txt_to_txt(folder_path)
