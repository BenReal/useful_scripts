# -*- coding: utf-8 -*-
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
import re
import pandas as pd

log_file_path = r'../logs/re_for_handling_filenames.log'
configure_logging(log_file_path)

# 记录日志信息
logging.info('Run Time Start up')
start_time = time.time()

folder_path = r"G:\资料检索\新建文件夹\台湾相关文献\pdf"

# 创建一个DataFrame用于存储处理后的数据
data = pd.DataFrame(columns=['文件ID', '文献名', '发布年份', '文件类型'])

temp = 0
# 遍历folder_path中的所有txt文件
for file_name in os.listdir(folder_path):

    # if temp > 1:
    #     break

    if file_name.endswith('.txt'):
        temp += 1
        file_path = os.path.join(folder_path, file_name)
        
        with open(file_path, 'r', encoding='utf8') as file:
            content = file.read()
            
            # 使用正则表达式提取数据
            pattern = r'(^abc\d{3}\.pdf=====)(.*?\n)([\w\W]*?)(?=^abc\d{3}\.pdf=====|\Z)'
            matches = re.findall(pattern, content, re.DOTALL | re.MULTILINE)
            
            # 将匹配到的数据添加到DataFrame中
            for match in matches:
                word_name_fit = match[2].replace('\n', ' ').replace('/', '-').replace('\\', '-').replace('|', '-').replace('?', ' ').replace('*', '#').replace('"', '_').replace('<', '_').replace('>', '_').replace(':', ' -- ').replace('�C', ' -- ')
                word_name_fit = word_name_fit.replace('  ', ' ').replace('  ', ' ').strip()
                file_item = {'文件ID': match[0].strip()[:6], '文献名': word_name_fit, '发布年份': match[1].strip(), '文件类型':r'.pdf'}
                print(file_item)
                data = data.append(file_item, ignore_index=True)


current_time = time.time()  # 获取当前时间的时间戳
current_time_tuple = time.localtime(current_time)  # 将时间戳转换为本地时间的struct_time元组
current_time_str = time.strftime(
    "%Y-%m-%d %H:%M:%S", current_time_tuple)  # 将struct_time元组转换为字符串格式
current_time_str = current_time_str.replace(':', '').replace(' ', '_')

excel_file_name = "处理结果_" + current_time_str + '.xlsx'

# 保存处理后的数据到Excel文件
output_file = os.path.join(folder_path, excel_file_name)
data.to_excel(output_file, index=False)


end_time = time.time()
run_time = end_time - start_time
print("程序运行时间：{}秒".format(run_time))
# 记录日志信息
logging.info('Run Time is over')
logging.info("Total running time: {} seconds".format(run_time))
