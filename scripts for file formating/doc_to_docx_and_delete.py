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
import logging
import time
from local_modules.local_functions import configure_logging
from win32com.client import Dispatch


log_file_path = r'../logs/app.log'
configure_logging(log_file_path)
# 记录日志信息
logging.info('程序开始运行')


def doc_to_docx(file_path, word):
    """
    将指定的doc文件转化为docx格式
    file_path: 文件路径
    word: 代表word应用程序
    """
    # 打开原始文档
    doc = word.Documents.Open(file_path)

    # 将文档另存为docx格式
    new_file_path = os.path.splitext(file_path)[0] + ".docx"
    doc.SaveAs(new_file_path, 16)

    # 关闭文档
    doc.Close()

    # 删除原始文件
    os.remove(file_path)

    # 打印操作过程
    print(f"{file_path}已经被成功转换为{new_file_path}")


def main():
    # 定义文件夹路径和Word应用程序对象
    folder_path = r"H:\《XXXX》《XXXX》2023年10月27日\研究成果——项目"
    word = Dispatch("Word.Application")

    num_files = 0
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.doc'):
                num_files += 1
    file_count = 0

    # 遍历文件夹中所有的.doc文件，并将其转换为.docx格式
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".doc"):
                file_path = os.path.join(root, file)
                doc_to_docx(file_path, word)
                file_count += 1
                # 打印统计结果
                print(f"进度：{file_count}/{num_files}，当前文件：{file}")

    # 关闭Word应用程序
    word.Quit()

    print("全部doc文件已经全部转换为docx!")


if __name__ == "__main__":
    main()


# 代码主要完成以下任务：
# 日志记录： 使用Python的logging模块配置日志记录，记录程序的运行信息。在这里，指定了日志文件名为'app.log'，记录级别为INFO，以及日志的格式。
# 批量将.doc文件转为.docx文件： 通过遍历指定文件夹中的所有.doc文件，使用Microsoft Word应用程序（通过win32com.client模块实现与Word的交互）将其转换为.docx格式。转换后的文件保存在原始文件的相同路径，并删除原始的.doc文件。
# 进度显示： 在转换过程中，输出当前转换的文件以及转换进度信息。
# Word应用程序的关闭： 在所有文件转换完成后，关闭与Word的交互所使用的Word应用程序。

# 代码的基本流程是：
# 配置日志记录。
# 使用Word应用程序对象打开指定文件夹中的所有.doc文件，将其转换为.docx格式，并在转换过程中输出进度信息。
# 关闭Word应用程序。
    
# 需要注意的是，代码中存在一个问题：日志配置的部分被重复定义了两次，这可能是因为复制粘贴时的错误。通常情况下，只需在程序开始时进行一次日志配置即可。可以删除其中一个配置部分，以避免重复。


