import os
import glob
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.probability import FreqDist
from nltk.tokenize import sent_tokenize
import pandas as pd
from datetime import datetime

# 导入预训练的句子分词模型
from nltk.tokenize.punkt import PunktSentenceTokenizer

# 创建句子分词器
sentence_tokenizer = PunktSentenceTokenizer()

# 定义函数来处理文本，提取关键词和生成摘要
def process_text(text):
    # 去除多余的换行符
    cleaned_text = re.sub(r'\n+', '\n', text)
    
    # 提取关键词
    tokens = text.split()  # 按空格分割文本为单词（保留原始的空格分隔）
    tokens = [token.lower() for token in tokens if token.lower() not in stopwords.words('english') and token.lower() not in string.punctuation]
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    fdist = FreqDist(stemmed_tokens)
    
    # 计算关键词数量
    text_length = len(tokens)
    num_keywords = max(3, text_length // 5000, 10)  # 每5000个词生成一个关键词，至少生成3个关键词
    keywords = fdist.most_common(num_keywords)  # 提取最常见的关键词
    
    # 生成摘要
    sentences = sentence_tokenizer.tokenize(cleaned_text)  # 使用句子分词器分割句子
    summary = ' '.join(sentences[:3])  # 取前3个句子作为摘要
    
    return keywords, summary

# 遍历目录树中的TXT文件
folder_path = 'G:\反无人机行业发展状况分析报告2023年12月7日\清单'  # 替换为实际的文件夹路径

results = []
total_files = 0
processed_files = 0

for root, dirs, files in os.walk(folder_path):
    total_files += len(glob.glob(os.path.join(root, '*.txt')))  # 统计每个文件夹下的TXT文件数量
    
for root, dirs, files in os.walk(folder_path):
    for file_name in files:
        if file_name.endswith('.txt'):
            file_path = os.path.join(root, file_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                    keywords, summary = process_text(text)
                    results.append((file_name, keywords, summary))
                    processed_files += 1
                    print(f"Processed file {processed_files}/{total_files}: {file_path}")
            except Exception as e:
                print(f"Error processing file: {file_path}")
                print(str(e))

# 构建输出文件名（包含时间戳）
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = os.path.join(folder_path, f'output_{timestamp}.xlsx')  # 添加时间戳到输出文件名，并使用与输入文件夹相同的路径

# 将结果保存到Excel文件
df = pd.DataFrame(results, columns=['文件名', '关键词', '摘要'])
df.to_excel(output_file, index=False)

print("Processing completed. Output file saved at:", output_file)
