import os
from PyPDF2 import PdfFileReader


target_dir = r"H:\资料检索：任务规划+火力筹划+火力协调+杀伤链+杀伤盒\资料pdf\3-其他资料"

# 获取当前目录下所有文件的文件名
files = os.listdir(target_dir)
# 对于每个文件，统计页数
for filename in files:
    if filename.endswith('.pdf'):
        file = os.path.join(target_dir, filename)
        try:
            with open(file, 'rb') as f:
                pdf = PdfFileReader(f)
                pages = pdf.getNumPages()
                print(f"{filename} 页数：{pages}")
        except:
            print(file)
            continue


