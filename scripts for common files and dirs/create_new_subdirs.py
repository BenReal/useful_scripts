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
dir_path = r"G:\蜂群战术\无人机项目"

# 要创建的子目录名称
subdirs = ["一、微型无人机-蜂群作战应用：山鹑、黄蜂等", "二、轻小型无人机-蜂群作战应用：郊狼等", "三、巡飞弹群-单体作战应用：LOCAAS、弹簧刀、英雄系列等", "八、其他无人机作战运用情况：小精灵、XQ-58、MQ-1C、苍鹭、MQ-9、大疆精灵4等", ]

# 在指定目录下创建子目录
for subdir in subdirs:
    subdir_path = os.path.join(dir_path, subdir)
    os.makedirs(subdir_path, exist_ok=True)
