import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import OPTICS
from datetime import datetime

# Prepare data
data = {'File Name': [], 'Group': []}

# Folder path
folder_path = r'H:\《XXXX》《XXXX》2023年10月27日\TXT文件\剩余（更新）'

# Walk through the directory tree
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith('.txt'):
            file_path = os.path.join(root, file)

            # Read file content
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                print(f"Error reading file {file}: {str(e)}")
                continue

            # Remove extra line breaks
            content = ' '.join(content.split())

            # Extract keywords and overview
            tokens = content.split()
            keywords = [word.lower() for word in tokens if word.isalpha()]
            overview = ' '.join(keywords[:200])  # Take the first 50 words as an overview

            data['File Name'].append(file)
            data['Group'].append(overview)

# Use OPTICS for text clustering
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data['Group'])

# Convert sparse matrix to dense
X_dense = X.toarray()

clustering = OPTICS(min_samples=5, xi=0.05, min_cluster_size=0.1)
data['Group'] = clustering.fit_predict(X_dense)

# Save the results to an Excel file
output_file = os.path.join(folder_path, f'results_optics_{datetime.now().strftime("%Y%m%d%H%M%S")}.xlsx')
df = pd.DataFrame(data)
df.to_excel(output_file, index=False)

print(f"Results saved to {output_file}")
