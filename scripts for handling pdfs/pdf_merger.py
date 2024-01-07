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
from PyPDF2 import PdfFileReader, PdfFileWriter


log_file_path = r'../logs/app.log'
configure_logging(log_file_path)
# 记录日志信息
logging.info('程序开始运行')


# 使用os模块的walk函数，搜索出指定目录下的全部PDF文件
# 获取同一目录下的所有PDF文件的绝对路径
def getFileName(filedir):

    file_list = [os.path.join(root, filespath) for root, dirs, files in os.walk(filedir) for filespath in files if str(filespath).endswith('pdf')]
    return file_list if file_list else []

# 合并同一目录下的所有PDF文件
def MergePDF(filepath, outfile):

    output = PdfFileWriter()
    outputPages = 0
    pdf_fileName = getFileName(filepath)
    table_contants = ''

    if pdf_fileName:
        for pdf_file in pdf_fileName:
            print("路径：%s" % pdf_file)

            # 读取源PDF文件
            input = PdfFileReader(open(pdf_file, "rb"))

            # 获得源PDF文件中页面总数
            pageCount = input.getNumPages()

            temp = pdf_file.split('\\')[-1] + '\t' + '----------' + str(outputPages+1) + '\n'
            table_contants += temp
            outputPages += pageCount

            print("页数：%d" % pageCount)

            # 分别将page添加到输出output中
            for iPage in range(pageCount):
                output.addPage(input.getPage(iPage))

        with open('abc', 'w',encoding='utf8') as f:
            f.write(table_contants)

        print("合并后的总页数:%d." % outputPages)
        # 写入到目标PDF文件
        outputStream = open(os.path.join(filepath, outfile), "wb")
        output.write(outputStream)
        outputStream.close()
        print("PDF文件合并完成！")

    else:
        print("没有可以合并的PDF文件！")


if __name__ == "__main__":
    time1 = time.time()
    file_dir = r'G:\merge' # 存放PDF的原文件夹
    outfile = "Cheat_Sheets.pdf" # 输出的PDF文件的名称
    MergePDF(file_dir, outfile)
    time2 = time.time()
    print('总共耗时：%s s.' % (time2 - time1))

