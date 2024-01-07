import os
import re
import shutil
import time
import pandas as pd
from pdfminer.high_level import extract_text
from pdfminer.high_level import extract_pages


# 注意：该脚本使用pdfminer模块，处理速度较慢。还需优化

# 设置要遍历的目录，windows下注意将反斜杠 "\" 统一替换为斜杠 "/"
root_dir = r"H:/无人侦察与火力突击运用案例情报资料"


# 设置要匹配的短语列表
phrase_list = [
"Vietnam",
"越南",
"Afghanistan",
"阿富汗",
"Soviet Union",
"苏联",
]


phrase_list = [i.lower() for i in phrase_list]
# print(phrase_list)

# 设置要移动的文件夹名
target_dir_name = "XXXXX"

# 创建一个空的DataFrame，用于保存结果
result_df = pd.DataFrame(columns=["文件名", "页数"] + phrase_list)

# 设置一个计数器，用于测试
counter_for_test = 0
token_for_test = False  # 初始化标记

# 遍历目录及其子目录下的所有PDF文件
for dirpath, dirnames, filenames in os.walk(root_dir):
    # print(dirpath)
    
    for filename in filenames:
        if filename.lower().endswith(".pdf"):            
            counter_for_test += 1

            # # 设置测试个数
            # if counter_for_test > 3:
            #     # print(counter_for_test)
            #     token_for_test = True
            #     break
            
            file_path = os.path.join(dirpath, filename)
            try:
                with open(file_path, 'rb') as fh:
                    num_pages = sum(1 for _ in extract_pages(fh))

                # 使用 PDFMiner 读取 PDF 文件
                text = extract_text(file_path).lower().replace("\n", '')
                # print(text)

                # 使用正则表达式统计短语出现次数
                phrase_counts = [0] * len(phrase_list)
                for j, keyword in enumerate(phrase_list):
                    phrase_counts[j] += len(re.findall(keyword, text))

                # 将结果保存到DataFrame中
                result_df.loc[len(result_df)] = [filename, num_pages] + phrase_counts

                # # 根据词频数，将相应文件移动到原目录下面的指定目录
                # if phrase_counts[0] > 0:
                #     target_dir_path = os.path.join(dirpath, target_dir_name)
                #     if not os.path.exists(target_dir_path):
                #         os.mkdir(target_dir_path)
                #     shutil.move(file_path, target_dir_path)
                
                # 打印结果
                print(f"处理第{counter_for_test}个文件：{filename} 页数：{num_pages}", end=' ')
                for i in range(len(phrase_list)):
                    print(f"{phrase_list[i]}：{phrase_counts[i]}", end=' ')
                print("\n", end='')

            except:
                print(f"第{counter_for_test}个文件存在未知问题：{file_path}")
                target_dir_path = os.path.join(dirpath, '未知问题文件')
                if not '未知问题文件' in dirpath:
                    if not os.path.exists(target_dir_path):
                        os.mkdir(target_dir_path)
                    try:
                        shutil.move(file_path, target_dir_path)
                    except:
                        print("文件已存在")
                        continue
                continue

    if token_for_test:
            break
    
current_time = time.time()  # 获取当前时间的时间戳
current_time_tuple = time.localtime(current_time)  # 将时间戳转换为本地时间的struct_time元组
current_time_str = time.strftime("%Y-%m-%d %H:%M:%S", current_time_tuple)  # 将struct_time元组转换为字符串格式
current_time_str = current_time_str.replace(':', '').replace(' ', '_')

# 设置保存结果的Excel文件名和工作表名
excel_file_name = "result_" + current_time_str +  '.xlsx'
sheet_name = "result"

dir_excel_file_name = os.path.join(root_dir, excel_file_name)

# 将结果保存到Excel文件中
with pd.ExcelWriter(dir_excel_file_name, engine="openpyxl", mode="w") as writer:
    result_df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"统计结果已保存到文件：{dir_excel_file_name} 中。")

