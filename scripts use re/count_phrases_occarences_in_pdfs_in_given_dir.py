import os
import re
import shutil
import time
import PyPDF2
import pandas as pd


# 设置要遍历的目录，windows下注意将反斜杠 "\" 统一替换为斜杠 "/"
root_dir = r"H:/无人侦察与火力突击运用案例情报资料"
# root_dir = "H:/【项目】/10-两个风洞项目2022年11月3日A/1-美欧风洞技术发展趋势分析及启示报告/未知问题文件1"

# 设置要匹配的短语列表
phrase_list = [
"Vietnam",
"越南",
"Afghanistan",
"阿富汗",
"Soviet Union",
"苏联",
"Israel",
"以色列",
]


phrase_list = [i.lower() for i in phrase_list]

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
                # 使用PyPDF2模块读取PDF文件，但无法处理中文
                with open(file_path, "rb") as f:
                    pdf_reader = PyPDF2.PdfFileReader(f, strict=False)
                    num_pages = pdf_reader.getNumPages()

                    # 使用正则表达式统计短语出现次数
                    phrase_counts = [0] * len(phrase_list)
                    for page in range(num_pages):
                        page_text = pdf_reader.getPage(page).extractText().lower()
                        # print(page_text)
                        for j, keyword in enumerate(phrase_list):
                            phrase_counts[j] += len(re.findall(keyword, page_text))


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


