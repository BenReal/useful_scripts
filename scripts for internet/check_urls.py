# -*- coding: utf-8 -*-
import os
import sys
# 获取当前脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
# print(script_dir)
# 如果当前目录是 'useful_scripts'，将当前目录加入搜索路径，否则，将父目录加入搜索路径
if os.path.basename(script_dir) == 'useful_scripts':
    sys.path.append(script_dir)
else:
    parent_dir = os.path.dirname(script_dir)
    sys.path.append(parent_dir)
# 导入其他模块
import requests
import subprocess

def read_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read().splitlines()

def validate_urls(urls):
    valid_urls = []
    for url in urls:
        try:
            response = requests.head(url, timeout=10)
            if response.status_code == 200:
                valid_urls.append(url)
                print(f"Valid url : {url}")
        except requests.ConnectionError:
            valid_urls.append(url)
            print(f"Connection error for {url}")

    return valid_urls

def save_valid_urls_to_file(valid_urls, output_file):
    with open(output_file, 'w') as file:
        for valid_url in valid_urls:
            file.write(valid_url + '\n')

def main():
    # subprocess.run('pwd')
    parent_dir = os.path.dirname(script_dir)
    # 使用 os.path.join 构建路径
    input_file = os.path.join(parent_dir, 'config', 'urls_for_check.txt')
    output_file = os.path.join(parent_dir, 'output', 'urls_valid.txt')

    try:
        urls_to_check = read_urls_from_file(input_file)
        valid_urls = validate_urls(urls_to_check)
        save_valid_urls_to_file(valid_urls, output_file)
        print("Validation complete. Valid URLs saved to", output_file)
    except Exception as e:
        print("An error occurred:", str(e))

if __name__ == "__main__":
    main()
