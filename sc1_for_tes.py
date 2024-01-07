import os
import zipfile
from tempfile import TemporaryDirectory

def remove_compatibility_mode(docx_path):
    temp_dir = TemporaryDirectory()
    temp_path = temp_dir.name

    with zipfile.ZipFile(docx_path, 'r') as zip_ref:
        zip_ref.extractall(temp_path)

    with zipfile.ZipFile(docx_path, 'w') as zip_ref:
        for root, dirs, files in os.walk(temp_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, temp_path)
                zip_ref.write(file_path, arcname)

    temp_dir.cleanup()

def batch_remove_compatibility_mode(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".docx"):
                docx_path = os.path.join(root, file)
                remove_compatibility_mode(docx_path)
                print(f"Removed compatibility mode for {docx_path}")

# 使用示例
folder_path = "H:/测试"  # 替换为你的文件夹路径
batch_remove_compatibility_mode(folder_path)
