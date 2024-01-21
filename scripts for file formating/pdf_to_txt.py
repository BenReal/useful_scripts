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

log_file_path = r'../logs/pdf_to_txt.log'
configure_logging(log_file_path)

# 记录日志信息
logging.info('程序开始运行')


# 指定要遍历的文件夹路径
folder_path = r"G:\资料检索\新建文件夹\新建文件夹\文献组_6"
folder_path = os.path.normpath(folder_path)


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


def convert_pdf_to_txt(folder_path):
    print(folder_path)
    num_files = 0
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".pdf") or file.endswith(".PDF"):
                num_files += 1

    file_count = 0

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # print(file)
            if file.endswith(".pdf") or file.endswith(".PDF"):
                # print(file)
                file_path = os.path.join(root, file)
                txt_file_path = os.path.splitext(file_path)[0] + ".txt"
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

                    # print(text)

                    with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
                        txt_file.write(text)

                except Exception as e:
                    print(f"Error converting {file}: {e}")
                    unknown_folder_path = os.path.join(folder_path, "未知问题文件")
                    os.makedirs(unknown_folder_path, exist_ok=True)
                    unknown_file_path = os.path.join(unknown_folder_path, file)
                    shutil.move(file_path, unknown_file_path)

                finally:
                    file_count += 1
                    print(f"转换进度：{file_count}/{num_files}，当前文件：{file}")


convert_pdf_to_txt(folder_path)


# 代码解析
# 需要安装**pdfminer.six**这个模块，而不是**pdfminer** 。pdfminer已经不再维护了，而pdfminer.six是它的一个更新版本，支持Python 3和Python 2。你可以在终端里运行这个命令来安装它：
# ```bash
# pip install pdfminer.six
# ```

# 然后，在你的代码里，你需要在`import pdfminer`这一行之后添加这一行：

# # 导入pdfminer和pdfminer.high_level模块
# import pdfminer
# import pdfminer.high_level

# # 使用extract_text函数提取PDF文件的文本
# text = pdfminer.high_level.extract_text("test.pdf")

# # 打印文本内容
# print(text)
# 这样，你就可以看到PDF文件的文本内容在终端里显示了。
