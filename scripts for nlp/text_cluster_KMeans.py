import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from datetime import datetime

def load_data(folder_path):
    data = {"File Name": [], "Text Content": []}

    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith(".txt"):
                file_path = os.path.join(root, filename)

                # 处理TXT文件
                with open(file_path, "r", encoding="utf-8") as file:
                    file_content = file.read()

                data["File Name"].append(filename)
                data["Text Content"].append(file_content)

    return pd.DataFrame(data)

def text_clustering(texts, num_clusters=3):
    # vectorizer = TfidfVectorizer(stop_words='english')
    vectorizer = TfidfVectorizer(stop_words='english', max_features=20000)

    X = vectorizer.fit_transform(texts)

    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(X)

    return kmeans, vectorizer

def get_cluster_info(data, kmeans, vectorizer):
    # 获取每个文本所属的簇
    cluster_assignments = kmeans.predict(vectorizer.transform(data['Text Content']))

    # 将结果添加到数据框中
    data['Cluster'] = cluster_assignments

    return data[['File Name', 'Cluster']]  # Only include 'File Name' and 'Cluster' columns

def main(folder_path):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_file = f"聚类_kmeans_{timestamp}.xlsx"
    output_file = os.path.join(folder_path, output_file)

    # 加载数据
    data = load_data(folder_path)

    # 聚类文本
    num_clusters = 50  # 可根据需要调整簇的数量
    kmeans, vectorizer = text_clustering(data['Text Content'], num_clusters)

    # 获取聚类信息
    clustered_data = get_cluster_info(data, kmeans, vectorizer)

    # 将结果保存到Excel文件
    clustered_data.to_excel(output_file, index=False)

# 以下是另一种策略

# def text_clustering(texts, num_clusters=3):
#     vectorizer = TfidfVectorizer(stop_words='english')
#     X = vectorizer.fit_transform(texts)

#     kmeans = KMeans(n_clusters=num_clusters, random_state=42)
#     kmeans.fit(X)

#     return kmeans, vectorizer, X

# def get_cluster_info(data, kmeans, vectorizer, X):
#     # 获取每个文本所属的簇
#     cluster_assignments = kmeans.predict(vectorizer.transform(data['Text Content']))

#     # 将结果添加到数据框中
#     data['Cluster'] = cluster_assignments

#     return data[['File Name', 'Cluster']]

# def main(folder_path):
#     timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
#     output_file = f"聚类_kmeans_{timestamp}.xlsx"
#     output_file = os.path.join(folder_path, output_file)

#     # 加载数据
#     data = load_data(folder_path)

#     # 聚类文本
#     num_clusters = 200
#     kmeans, vectorizer, X = text_clustering(data['Text Content'], num_clusters)

#     # 获取聚类信息
#     batch_size = 100  # Set an appropriate batch size
#     start = 0
#     while start < len(data):
#         end = start + batch_size
#         batch_data = data.iloc[start:end]
#         batch_X = X[start:end, :]
#         clustered_data = get_cluster_info(batch_data, kmeans, vectorizer, batch_X)

#         # Append or save the clustered_data to a result file (e.g., Excel, CSV)
#         if start == 0:
#             clustered_data.to_excel(output_file, index=False)
#         else:
#             clustered_data.to_excel(output_file, index=False, mode='a', header=False)

#         start = end


if __name__ == "__main__":
    try:
        folder_path = "H:\《XXXX》《XXXX》2023年10月27日\TXT文件\剩余（更新）"
        # folder_path = "G:\反无人机行业发展状况分析报告2023年12月7日\反无人机"
        print("Processing files in the folder:")
        main(folder_path)
        print("Processing completed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


