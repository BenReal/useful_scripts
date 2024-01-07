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
import docx
from hanziconv import HanziConv


log_file_path = r'../logs/app.log'
configure_logging(log_file_path)

# 记录日志信息
logging.info('程序开始运行')


def convert_docx_to_txt(path):
    """
    将指定路径下的docx文件转换成txt文件
    :param path: 文件路径
    """
    # 获取文件名和扩展名
    filename, ext = os.path.splitext(path)

    txt_path = filename + '.txt'

    # 判断文件扩展名是否为docx
    if ext.lower() == '.docx':
        try:
            doc = docx.Document(path)
            with open(txt_path, 'w', encoding='utf-8') as f:
                for para in doc.paragraphs:
                    f.write(HanziConv.toSimplified(para.text))
                    f.write('\n')
        except:
            print(f"转换失败：{path}")

    # 如果文件扩展名不为doc或docx，则返回空字符串
    else:
        return ''


def convert_all_docs_to_txt(path):
    """
    将指定路径下的所有docx文件转换成txt文件
    :param path: 文件路径
    """
    num_files = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.docx'):
                num_files += 1

    file_count = 0

    # 遍历路径下的所有文件和子文件夹
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.docx'):
                file_count += 1
                # 打印统计结果
                print(f"进度：{file_count}/{num_files}，当前文件：{file}")

            # 获取文件路径
            file_path = os.path.join(root, file)

            # 将docx文件转换成txt文件
            convert_docx_to_txt(file_path)


def main():
    # 指定文件夹路径
    folder_path = r"H:\《XXXX》《XXXX》2023年10月27日\研究成果——项目"

    # 将所有docx文件转换成txt文件
    convert_all_docs_to_txt(folder_path)


if __name__ == '__main__':
    main()
