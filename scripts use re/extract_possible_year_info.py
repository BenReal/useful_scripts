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
import re
import pandas as pd
import logging
import time
from local_modules.local_functions import configure_logging


configure_logging(r'../logs/extract_possible_year_info.log')

YEAR_PATTERN_WORD = r'\b(?:19[5-9]\d|20\d{2})\b'
YEAR_PATTERN = r'(?:19[5-9]\d|20\d{2})'


def process_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf8') as file:
            content = file.read()
            file_length = len(content)

            head_1A_matches = re.findall(YEAR_PATTERN_WORD, content[:1000])
            head_2A_matches = re.findall(YEAR_PATTERN_WORD, content[1000:2000])
            head_3A_matches = re.findall(YEAR_PATTERN_WORD, content[2000:3000])
            head_4A_matches = re.findall(YEAR_PATTERN_WORD, content[3000:4000])

            head_1B_matches = re.findall(YEAR_PATTERN, content[:1000])
            head_2B_matches = re.findall(YEAR_PATTERN, content[1000:2000])
            head_3B_matches = re.findall(YEAR_PATTERN, content[2000:3000])
            head_4B_matches = re.findall(YEAR_PATTERN, content[3000:4000])


            return {"head_1A": head_1A_matches, "head_2A": head_2A_matches, "head_3A": head_3A_matches, "head_4A": head_4A_matches, "head_1B": head_1B_matches, "head_2B": head_2B_matches, "head_3B": head_3B_matches, "head_4B": head_4B_matches, }

    except Exception as e:
        logging.error(f"Error processing file {file_path}: {str(e)}")
        return None

def main():
    start_time = time.time()

    root_folder = r'H:\新建文件夹'
    excel_output_dir = r'H:\新建文件夹'    
   
    timestamp = time.strftime("%Y%m%d%H%M%S")
    excel_output_path = os.path.join(excel_output_dir, f'extract_possible_year_{timestamp}.xlsx')

    df_data = {'File': [], "head_1A": [], "head_2A": [], "head_3A": [], "head_4A": [], "head_1B": [], "head_2B": [], "head_3B": [], "head_4B": [], }

    os.makedirs(excel_output_dir, exist_ok=True)

    for folder, _, files in os.walk(root_folder):
        for file in files:
            if file.lower().endswith('.txt'):
                file_path = os.path.join(folder, file)
                file_result = process_file(file_path)
                if file_result:
                    df_data['File'].append(file_path)
                    df_data['head_1A'].append(file_result['head_1A'])
                    df_data['head_2A'].append(file_result['head_2A'])
                    df_data['head_3A'].append(file_result['head_3A'])
                    df_data['head_4A'].append(file_result['head_4A'])
                    df_data['head_1B'].append(file_result['head_1B'])
                    df_data['head_2B'].append(file_result['head_2B'])
                    df_data['head_3B'].append(file_result['head_3B'])
                    df_data['head_4B'].append(file_result['head_4B'])

    df_result = pd.DataFrame(df_data)
    df_result.to_excel(excel_output_path, index=False, engine='xlsxwriter')

    end_time = time.time()
    run_time = end_time - start_time

    print("程序运行时间：{}秒".format(run_time))
    logging.info("程序运行时间：{}秒".format(run_time))

if __name__ == "__main__":
    main()
