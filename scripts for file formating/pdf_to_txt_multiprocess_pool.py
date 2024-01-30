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
import re
from local_modules.local_functions import configure_logging
from pdfminer.high_level import extract_text
from hanziconv import HanziConv
from zenhan import z2h
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


def remove_empty_lines(text):
    lines = text.split('\n')
    non_empty_lines = [line for line in lines if line.strip() != '']
    return '\n'.join(non_empty_lines)


def process_extracted_text(text):
    # 全部转换成半角字符
    text = z2h(text)
    # 将中文转为简体
    text = HanziConv.toSimplified(text)
    # 统一换行符格式
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    # 处理多余的空格
    text = re.sub("  +", " ", text)
    # 删除中文字符后的空格
    text = remove_spaces_after_chinese(text)
    # 去除多余的空行
    text = remove_empty_lines(text)
    return text


def convert_pdf_to_txt(file_path):
    try:
        text = extract_text(file_path)
        text = process_extracted_text(text)

        file_name = os.path.basename(file_path)
        pdf_directory = os.path.dirname(file_path)
        txt_file_path = os.path.join(pdf_directory, os.path.splitext(file_name)[0] + ".txt")

        with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text)

        process_name = multiprocessing.current_process().name
        print(f"进程 {process_name} 完成转换：{file_path}")

    except Exception as e:
        print(f"Error converting {file_path}: {e}")
        file_name = os.path.basename(file_path)
        pdf_directory = os.path.dirname(file_path)
        exception_folder_path = os.path.join(pdf_directory, "未知问题文件")
        # if not os.path.exists(exception_folder_path):
        #     os.makedirs(exception_folder_path)
        os.makedirs(exception_folder_path, exist_ok=True)
        exception_file_path = os.path.join(exception_folder_path, file_name)
        shutil.move(file_path, exception_file_path)
    # finally:
    #     print(f"完成转换：{file_path}")


def convert_pdf_to_txt_parallel(file_path):
    try:
        convert_pdf_to_txt(file_path)
    except Exception as e:
        print(f"Error processing {file_path}: {e}")


if __name__ == '__main__':
    multiprocessing.freeze_support()  # Add this line
    folder_path = r"F:\总备份\文献库\S类文献（pdf+txt）\美国空军出版物"
    folder_path = os.path.normpath(folder_path)

    file_list = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".pdf"):
                file_path = os.path.join(root, file)
                file_list.append(file_path)

    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        pool.map(convert_pdf_to_txt_parallel, file_list)

    print("转换完成")


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

