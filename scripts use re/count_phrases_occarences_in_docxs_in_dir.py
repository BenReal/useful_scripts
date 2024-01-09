import os
import re
import pandas as pd
from docx import Document

# 定义要统计的短语列表
phrases = ["intelligence department", "information", "plan"]

# 创建一个空的DataFrame用于存储统计结果
df = pd.DataFrame(columns=["文件名", "页数"] + phrases)

# 定义递归遍历目录的函数


def traverse_dir(dir_path):
    for root, dirs, files in os.walk(dir_path):
        for filename in files:
            full_path = os.path.join(root, filename)
            if filename.endswith(".docx"):
                # 统计出现次数和页数
                doc = Document(full_path)
                total_pages = len(doc.sections)
                count_dict = {phrase: 0 for phrase in phrases}
                for paragraph in doc.paragraphs:
                    text = paragraph.text.lower()
                    for phrase in phrases:
                        count_dict[phrase] += len(re.findall(phrase, text))

                # 打印结果
                print(f"文件 {filename} 共有 {total_pages} 页，短语出现次数如下:")
                for phrase in phrases:
                    print(f"{phrase}: {count_dict[phrase]}")

                # 将结果添加到DataFrame中
                row_data = [filename, total_pages] + \
                    [count_dict[phrase] for phrase in phrases]
                df.loc[len(df)] = row_data

    # 保存Excel文件
    output_file = os.path.join(dir_path, "word_count.xlsx")
    df.to_excel(output_file, index=False)
    print(f"统计结果已保存到文件 {output_file}")


# 开始遍历目录
dir_path = r"H:/abc"
traverse_dir(dir_path)
