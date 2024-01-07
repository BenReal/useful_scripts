import os
import re
import time
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from gensim.parsing.preprocessing import preprocess_string

def clean_text(text):
    # 清理文本，去除多余的换行符
    return ' '.join(preprocess_string(text))


def extract_keywords_tfidf(text, num_keywords=5):
    # 提取关键词使用 TF-IDF 算法

    # 创建一个 TF-IDF 向量化器，指定停用词为英语停用词
    # vectorizer = TfidfVectorizer(stop_words='english')
    
    # 另一种方式：指定停用词为英语停用词，并限制最大特征数为5000
    vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)

    # 对输入的文本进行 TF-IDF 向量化
    tfidf_matrix = vectorizer.fit_transform([text])

    # 获取特征名字，即单词列表
    feature_names = vectorizer.get_feature_names()

    # 将 TF-IDF 矩阵转换为数组，并获取每个词的 TF-IDF 得分
    tfidf_scores = dict(zip(feature_names, tfidf_matrix.toarray()[0]))

    # 选择得分最高的 num_keywords 个词作为关键词
    keywords = sorted(tfidf_scores.items(), key=lambda x: x[1], reverse=True)[:num_keywords]

    # 返回关键词列表
    return [word for word, _ in keywords]


def calculate_num_keywords(text):
    num_words = sum(1 for _ in re.finditer(r'\b\w+\b', text))
    return max(min(int(num_words / 5000), 20), 5)

def count_txt_files(folder):
    # 统计目录树中的 .txt 文件总数
    count = 0
    for _, _, files in os.walk(folder):
        count += len([file for file in files if file.endswith('.txt')])
    return count

def process_folder(input_folder, output_folder):
    total_txt_files = count_txt_files(input_folder)
    data = {'File Name': [], 'Keywords': []}

    txt_file_count = 0
    
    for i, (folder_path, _, files) in enumerate(os.walk(input_folder)):
        for j, file in enumerate(files):
            file_path = os.path.join(folder_path, file)
            if file.endswith('.txt'):
                txt_file_count += 1
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text = clean_text(f.read())
                        num_keywords = calculate_num_keywords(text)
                        keywords_result = extract_keywords_tfidf(text, num_keywords=num_keywords)

                        data['File Name'].append(file)
                        data['Keywords'].append(keywords_result)

                    print(f'Processed file {txt_file_count}/{total_txt_files}: {file_path}')
                except Exception as e:
                    print(f'Error processing file {file}: {str(e)}')

    df = pd.DataFrame(data)
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_filename = os.path.join(output_folder, f'关键词_tf-idf_{timestamp}.xlsx')
    df.to_excel(output_filename, index=False)
    print(f'Output saved to {output_filename}')

if __name__ == "__main__":
    input_folder = 'H:\《XXXX》《XXXX》2023年10月27日\TXT文件'
    output_folder = 'H:\《XXXX》《XXXX》2023年10月27日\TXT文件'
    
    try:
        process_folder(input_folder, output_folder)
    except Exception as e:
        print(f'Error: {str(e)}')
