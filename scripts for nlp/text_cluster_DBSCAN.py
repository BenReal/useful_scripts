import os
import glob
import pandas as pd
from nltk import word_tokenize
from nltk.corpus import stopwords  # Add this import
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN
from datetime import datetime

# 设置停用词
stop_words = set(stopwords.words('english'))

# 准备数据
data = {'File Name': [], 'Group': []}

# 文件夹路径
folder_path = r'H:\《XXXX》《XXXX》2023年10月27日\TXT文件\剩余（更新）'

# 遍历目录树
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith('.txt'):
            file_path = os.path.join(root, file)

            # 读取文件内容
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                print(f"Error reading file {file}: {str(e)}")
                continue

            # 移除多余换行符
            content = ' '.join(content.split())

            # 提取关键词和概述
            tokens = word_tokenize(content)
            keywords = [word.lower() for word in tokens if word.isalpha() and word.lower() not in stop_words]
            overview = ' '.join(keywords[:200])  # 取前50个词作为概述

            data['File Name'].append(file)
            data['Group'].append(overview)

# 使用DBSCAN进行文本聚类
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data['Group'])

clustering = DBSCAN(eps=0.5, min_samples=5)
data['Group'] = clustering.fit_predict(X)

# 将结果保存到Excel文件
output_file = os.path.join(folder_path, f'聚类_dbscan_{datetime.now().strftime("%Y%m%d%H%M%S")}.xlsx')
df = pd.DataFrame(data)
df.to_excel(output_file, index=False)

print(f"Results saved to {output_file}")
