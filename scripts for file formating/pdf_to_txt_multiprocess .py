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
from pdfminer.high_level import extract_text
from hanziconv import HanziConv
import multiprocessing


log_file_path = r'../logs/app.log'
configure_logging(log_file_path)

# 记录日志信息
logging.info('程序开始运行')


def is_chinese_character(char):
    unicode_value = ord(char)
    if 0x4E00 <= unicode_value <= 0x9FFF:
        return True
    else:
        return False

# def is_chinese_character(char):
#     return 0x4E00 <= ord(char) <= 0x9FFF

# 在这个优化的版本中，使用列表 result 来存储每个字符，而不是使用字符串拼接操作。这是因为在 Python 中，字符串是不可变对象，每次拼接字符串都会创建一个新的字符串对象，导致性能下降。使用列表存储字符，最后使用 join 方法将列表中的字符连接成一个新的字符串，可以避免这个问题。
# 此外，还将 result 声明为列表，而不是字符串。这样可以避免在每次追加字符时都创建一个新的字符串对象，提高效率。
def remove_spaces_after_chinese(text):
    result = []
    i = 0
    while i < len(text):
        char = text[i]
        if is_chinese_character(char):
            result.append(char)
            i += 1
            while i < len(text) and text[i] == " ":
                i += 1
        else:
            result.append(char)
            i += 1
            if i < len(text) and text[i] == " ":
                while i < len(text) and text[i] == " ":
                    i += 1
    return ''.join(result)

# def remove_spaces_after_chinese(text):
#     result = ""
#     i = 0
#     while i < len(text):
#         char = text[i]
#         if is_chinese_character(char):
#             result += char
#             i += 1
#             while i < len(text) and text[i] == " ":
#                 i += 1
#         else:
#             result += char
#             i += 1
#     return result


def remove_empty_lines(text):
    # 去除空行
    lines = text.split('\n')
    non_empty_lines = [line for line in lines if line.strip() != '']
    return '\n'.join(non_empty_lines)

# 在这个优化的版本中，使用了 filter 函数来过滤掉空行，而不是使用列表推导式。filter 函数接受一个函数和一个可迭代对象作为参数，返回一个迭代器，其中包含满足给定函数条件的元素。
# 通过使用 filter 函数，避免了创建一个完整的列表，而是直接返回一个迭代器。这样可以节省内存，并且在这个版本中不需要额外的列表推导式。
# def remove_empty_lines(text):
#     # 去除空行
#     lines = text.split('\n')
#     non_empty_lines = filter(lambda line: line.strip() != '', lines)
#     return '\n'.join(non_empty_lines)

def convert_pdf_to_txt(file_path):
    try:
        text = extract_text(file_path)
        text = remove_empty_lines(text)
        text = text.translate(str.maketrans(
            "０１２３４５６７８９　ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ",
            "0123456789 ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        ))

        # 删除中文字符后的空格
        text = remove_spaces_after_chinese(text)

        # 将中文转为简体
        text = HanziConv.toSimplified(text)

        # 获取文件名
        file_name = os.path.basename(file_path)
        pdf_directory = os.path.dirname(file_path)
        txt_file_path = os.path.join(pdf_directory, os.path.splitext(file_name)[0] + ".txt")

        with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text)

        # 打印进程和文件信息
        process_name = multiprocessing.current_process().name
        print(f"进程 {process_name} 完成转换：{file_path}")

    except Exception as e:
        print(f"Error converting {file_path}: {e}")
        unknown_folder_path = os.path.join(folder_path, "未知问题文件")
        os.makedirs(unknown_folder_path, exist_ok=True)
        unknown_file_path = os.path.join(unknown_folder_path, file_name)
        shutil.move(file_path, unknown_file_path)
    finally:
        print(f"完成转换：{file_path}")


def process_files(file_list):
    for file_path in file_list:
        convert_pdf_to_txt(file_path)

def convert_pdf_to_txt_parallel(folder_path):
    file_list = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".pdf") or file.endswith(".PDF"):
                file_path = os.path.join(root, file)
                file_list.append(file_path)

    num_processes = multiprocessing.cpu_count()
    chunk_size = len(file_list) // num_processes

    processes = []
    for i in range(num_processes):
        start_index = i * chunk_size
        end_index = (i + 1) * chunk_size if i < num_processes - 1 else len(file_list)
        process_files_list = file_list[start_index:end_index]
        process = multiprocessing.Process(target=process_files, args=(process_files_list,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    print("转换完成")

if __name__ == '__main__':
    multiprocessing.freeze_support()  # Add this line
    folder_path = r"F:\XXXX\手机软件"
    folder_path = os.path.normpath(folder_path)
    convert_pdf_to_txt_parallel(folder_path)


# 代码解析
# 需要安装**pdfminer.six**这个模块，而不是**pdfminer** 。pdfminer已经不再维护了，而pdfminer.six是它的一个更新版本，支持Python 3和Python 2。可以在终端里运行这个命令来安装它：
# ```bash
# pip install pdfminer.six
# ```

# 然后，在的代码里，需要在`import pdfminer`这一行之后添加这一行：

# # 导入pdfminer和pdfminer.high_level模块
# import pdfminer
# import pdfminer.high_level

# # 使用extract_text函数提取PDF文件的文本
# text = pdfminer.high_level.extract_text("test.pdf")

# # 打印文本内容
# print(text)
# 这样，就可以看到PDF文件的文本内容在终端里显示了。

