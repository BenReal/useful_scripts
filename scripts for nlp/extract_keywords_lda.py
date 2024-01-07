import os
import re
import time
import pandas as pd
from gensim import corpora
from gensim.models import LdaModel
from gensim.parsing.preprocessing import preprocess_string

def clean_text(text):
    # 清理文本，去除多余的换行符
    return ' '.join(preprocess_string(text))

def extract_keywords(text, num_topics=5, num_keywords=5):
    # 提取关键词
    texts = [text.split()]
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    lda_model = LdaModel(corpus, num_topics=num_topics, id2word=dictionary)
    topics = lda_model.show_topics(num_topics=num_topics, num_words=num_keywords, formatted=False)

    return [word for topic in topics for word, _ in topic[1]]

def calculate_num_keywords(text):
    num_words = sum(1 for _ in re.finditer(r'\b\w+\b', text))
    return max(min(int(num_words / 5000), 20), 5)

def count_txt_files(folder):
    # 统计目录树中的 .txt 文件总数
    count = 0
    for _, _, files in os.walk(folder):
        count += len([file for file in files if file.endswith('.txt')])
    return count

# ... (previous code)

def process_folder(input_folder, output_folder, num_topics_range):
    total_txt_files = count_txt_files(input_folder)
    data = {'File Name': []}

    for num_topics in num_topics_range:
        data[f'Keywords_{num_topics}'] = []

    for i, (folder_path, _, files) in enumerate(os.walk(input_folder)):
        for j, file in enumerate(files):
            file_path = os.path.join(folder_path, file)
            if file.endswith('.txt'):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text = clean_text(f.read())
                        num_keywords = calculate_num_keywords(text)

                        file_keywords = {'File Name': file}

                        for num_topics in num_topics_range:
                            keywords_result = extract_keywords(text, num_topics=num_topics, num_keywords=num_keywords)
                            file_keywords[f'Keywords_{num_topics}'] = keywords_result

                        data['File Name'].append(file)
                        for num_topics in num_topics_range:
                            data[f'Keywords_{num_topics}'].append(file_keywords[f'Keywords_{num_topics}'])

                    print(f'Processed file {j + 1}/{len(files)} in directory {i + 1}/{total_txt_files}: {file_path}')
                except Exception as e:
                    print(f'Error processing file {file}: {str(e)}')

    df = pd.DataFrame(data)

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_filename = os.path.join(output_folder, f'关键词_LDA_{timestamp}.xlsx')
    df.to_excel(output_filename, index=False)
    print(f'Output saved to {output_filename}')

if __name__ == "__main__":
    input_folder = 'H:\《XXXX》《XXXX》2023年10月27日\TXT文件'
    output_folder = 'H:\《XXXX》《XXXX》2023年10月27日\TXT文件'
    num_topics_range = range(5, 80, 5)
    
    try:
        process_folder(input_folder, output_folder, num_topics_range)
    except Exception as e:
        print(f'Error: {str(e)}')
