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


log_file_path = r'../logs/app.log'
configure_logging(log_file_path)

# 记录日志信息
logging.info('程序开始运行')

# 指定目录
dir_path = r"H:\新型作战力量、联合作战动态战斗任务规划等研究综述专题报告"

# 要创建的子目录名称
subdirs = ["1、美军新质作战力量建设未来发展分析报告定制版", "2、联合作战动态战斗任务规划技术发展研究定制版", "3、作战筹划和效能评估整编报告定制版", "4、美军作战任务规划系统组成调研报告定制版", "5、美军新型杀伤链 杀伤网建设情况分析报告定制版", ]

# 在指定目录下创建子目录
for subdir in subdirs:
    subdir_path = os.path.join(dir_path, subdir)
    os.makedirs(subdir_path, exist_ok=True)
