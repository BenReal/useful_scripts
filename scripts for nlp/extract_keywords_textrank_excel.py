import pandas as pd
from gensim.summarization import keywords
import jieba
from datetime import datetime
import os
import re

with open("./config/stop_words_cn.txt", "r", encoding="utf8") as f_cn:
    stop_words_cn = [line.strip() for line in f_cn.readlines() if line.strip()]

with open("./config/stop_words_en.txt", "r", encoding="utf8") as f_en:
    stop_words_en = [line.strip() for line in f_en.readlines() if line.strip()]

def extract_keywords_cn(text):
    # 对中文文本进行分词
    words = jieba.cut(text)
    # 将分词结果转换为字符串，以空格分隔
    tokenized_text = " ".join(words)
    # 使用 gensim 的 keywords 函数提取关键词
    kw = keywords(tokenized_text, ratio=1, split=True)
    return kw

def extract_keywords_en(text):
    # 使用 gensim 的 keywords 函数提取关键词
    kw = keywords(text, ratio=1, split=True)
    return kw

def words_cn(text):
    words = list(jieba.cut(text))
    words = [i for i in words if i not in stop_words_cn and i]
    return sorted(words)

def words_en(text):
    words = re.findall(r"\b\w+\b", text)
    words = [i for i in words if i not in stop_words_en and i]
    return sorted(words) 

def save_with_timestamp(output_directory, file_prefix, file_extension='xlsx'):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f"{file_prefix}_{timestamp}.{file_extension}"
    return os.path.join(output_directory, file_name)

# 输入和输出文件路径
input_path = r'H:\《XXXX》《XXXX》2023年10月27日\分类工作表2023年12月16日A'
input_file = r'文件名.xlsx' 
output_directory = r'H:\《XXXX》《XXXX》2023年10月27日\分类工作表2023年12月16日A'

input_file_path = os.path.join(input_path, input_file)


# 读取Excel文件
df = pd.read_excel(input_file_path)

# 提取关键词并添加到 DataFrame 中，第一列是ID，第二列是英文标题，第三列是中文标题
# 在 pandas 中，列的序号是从 0 开始计算的，因此第一列的序号是 0，第二列的序号是 1，以此类推。这是因为 pandas 使用基于零的索引，与 Python 中的列表和其他数据结构一致。所以，在使用 iloc 进行索引时，记得从 0 开始计数。
df['English_Keywords'] = df.iloc[:, 1].apply(extract_keywords_en)
df['English_no_stop'] = df.iloc[:, 1].apply(words_en)
df['Chinese_Keywords'] = df.iloc[:, 2].apply(extract_keywords_cn)
df['Chinese_no_stop'] = df.iloc[:, 2].apply(words_cn)


# 生成输出文件路径
output_file_path = save_with_timestamp(output_directory, 'excel_keywords')

# 保存处理后的DataFrame到新的Excel文件
df.to_excel(output_file_path, index=False)

print(f"Results saved to: {output_file_path}")


