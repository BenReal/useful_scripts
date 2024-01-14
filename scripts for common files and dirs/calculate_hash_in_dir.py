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
import hashlib
from pathlib import Path
import pandas as pd
from multiprocessing import Pool, Manager
from functools import wraps
import time
from local_modules.local_functions import add_timestamp

def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Total time taken: {elapsed_time:.2f} seconds")
        return result
    return wrapper

def process_file(file_path, result_dict):
    try:
        with open(file_path, "rb") as f:
            content = f.read()
            sha256_hash = hashlib.sha256(content).hexdigest()
            result_dict[file_path] = sha256_hash
    except Exception as e:
        result_dict[file_path] = str(e)
        
@timing_decorator
def main():
    input_directory_path = Path("/Users/zhishui/god/【英语】/中英对照")
    output_directory_path = Path("/Users/zhishui/god/【英语】/中英对照")
    file_type = r'.pdf'
    # file_type = r'.txt'
    result_dict = Manager().dict()

    # Using Pool for multiprocessing
    with Pool() as pool:
        files = [file for file in input_directory_path.rglob("*") if file.is_file() and file.suffix.lower() == file_type]
        pool.starmap(process_file, [(file, result_dict) for file in files])

    # list(result_dict.items()) 会得到一个包含 result_dict 中所有键值对的列表。具体来说，result_dict.items() 返回一个由键值对组成的视图对象，然后通过 list() 转换成列表。
    # 每个键值对是一个元组，形式为 (key, value)。这个操作将字典的所有键值对转化为一个列表，其中每个元素都是字典中的一个键值对。
    df = pd.DataFrame(list(result_dict.items()), columns=['File', 'SHA-256'])

    # Save DataFrame to Excel in the specified output directory
    excel_path = output_directory_path / "文件哈希值.xlsx"
    excel_path = add_timestamp(excel_path)

    df.to_excel(excel_path, index=False)
    print(f"Results saved to {excel_path}")

if __name__ == "__main__":
    main()
