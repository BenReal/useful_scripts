import os
import re
import time
import pandas as pd
from gensim.summarization import keywords

def clean_text(text):
    # 清理文本，去除多余的换行符
    cleaned_text = re.sub(r'\n{2,}', '\n', text)
    return cleaned_text

def extract_keywords(text):
    # 提取关键词及其权重
    # return [(word, f'{weight:.2f}') for word, weight in keywords(text, scores=True)]
    # return keywords(text).split(', ')
    return [word for word, weight in keywords(text, scores=True)]

# def calculate_num_keywords(text):
#     # 使用正则表达式匹配单词，并计算单词数量
#     words = re.findall(r'\b\w+\b', text)
#     num_words = len(words)

#     # 计算关键词数量，这里使用一个简单的非线性函数
#     return max(min(int(num_words / 5000), 20), 5)

def calculate_num_keywords(text):
    num_words = sum(1 for _ in re.finditer(r'\b\w+\b', text))
    return max(min(int(num_words / 5000), 20), 5)


def count_txt_files(folder):
    # 统计目录树中的 .txt 文件总数
    count = 0
    for _, _, files in os.walk(folder):
        count += len([file for file in files if file.lower().endswith('.txt')])
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
                        # 这里计算关键词数量的方法有问题，输入的是整个文本的中字符数量，而不是单词数量。修妖进行修改。
                        # num_keywords = calculate_num_keywords(len(text))
                        num_keywords = calculate_num_keywords(text)
                        keywords_result = extract_keywords(text)[:num_keywords]
                        data['File Name'].append(file)
                        data['Keywords'].append(keywords_result)

                    print(f'Processed file {txt_file_count}/{total_txt_files}: {file_path}')
                except Exception as e:
                    print(f'Error processing file {file}: {str(e)}')

    df = pd.DataFrame(data)
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_filename = os.path.join(output_folder, f'关键词_textrank_{timestamp}.xlsx')
    df.to_excel(output_filename, index=False)
    print(f'Output saved to {output_filename}')


if __name__ == "__main__":
    input_folder = 'H:\《XXXX》《XXXX》2023年10月27日\TXT文件'
    output_folder = 'H:\《XXXX》《XXXX》2023年10月27日\TXT文件'
    
    try:
        process_folder(input_folder, output_folder)
    except Exception as e:
        print(f'Error: {str(e)}')


# 注意
# 从Gensim 4.x版本开始，gensim.summarization模块已被删除，因为它是一个未维护的第三方模块。仍想使用gensim.summarization.summarize，需要降低gensim的版本，例如3.8.2。例如：pip3 install "gensim==3.8.2"。

# gensim 库的 keywords 函数使用TextRank算法来提取文本中的关键词。TextRank是一种图算法，基于PageRank算法的思想。它通过构建单词之间的图网络，利用单词之间的关系计算每个单词的重要性，从而提取关键词。
# gensim 中的 keywords 函数有一些可选参数，但主要参数是输入的文本字符串。以下是 keywords 函数的基本签名：

# gensim.summarization.keywords(text, ratio=0.2, words=None, split=False, scores=False, pos_filter=('NN', 'JJ'), lemmatize=True, deacc=False)
        
# 主要参数：
# text: 要提取关键词的输入文本字符串。
# ratio：关键词数量相对于原始文本的比例。默认为0.2。
# words：指定要提取的关键词的数量，如果提供此参数，ratio 将被忽略。
# split：如果为True，返回关键词的列表而不是字符串。默认为False。
# scores：如果为True，返回关键词及其权重的列表。默认为False。
# pos_filter：一个元组，包含要保留的词性标签（例如，'NN' 表示名词，'JJ' 表示形容词）。默认为 ('NN', 'JJ')。
# lemmatize：如果为True，对单词进行词形还原。默认为True。
# deacc：如果为True，去除字符串中的重音符号。默认为False。

