import os
import shutil
import pandas as pd

def find_file(source_folder, file_name):
    for folder_path, _, files in os.walk(source_folder):
        for file in files:
            if file.lower() == file_name.lower():
                return os.path.join(folder_path, file)
    return None

def create_folder_structure(root_folder, folders):
    current_folder = root_folder
    for folder in folders:
        current_folder = os.path.join(current_folder, folder)
        if not os.path.exists(current_folder):
            os.makedirs(current_folder)
    print(f"Created folder structure: {current_folder}")

def copy_files(source_folder, target_folder, file_names):
    success_count = 0
    failure_count = 0
    failure_list = []

    for file_name in file_names:
        source_path = find_file(source_folder, file_name)
        if source_path:
            target_path = os.path.join(target_folder, file_name)
            try:
                shutil.copy2(source_path, target_path)
                print(f"Copied file: {file_name} to {target_folder}")
                success_count += 1
            except Exception as e:
                print(f"Error copying file: {file_name}. {str(e)}")
                failure_count += 1
                failure_list.append(file_name)
        else:
            print(f"File not found: {file_name}. Skipped.")
            failure_count += 1
            failure_list.append(file_name)

    return success_count, failure_count, failure_list

def process_row(source_folder, target_root_folder, row):
    success_total = 0
    failure_total = 0
    failure_list_total = []

    for i in range(1, len(row), 3):
        target_folders = row[i:i+3].dropna().tolist()
        target_folder_path = os.path.join(target_root_folder, *target_folders)
        create_folder_structure(target_root_folder, target_folders)
        success, failure, failure_list = copy_files(source_folder, target_folder_path, [row[0]])
        success_total += success
        failure_total += failure
        failure_list_total.extend(failure_list)

    return success_total, failure_total, failure_list_total

def main():
    # 读取Excel文件
    excel_path = "./useful_scripts/config/move_file_specific.xlsx"
    df = pd.read_excel(excel_path)

    # 获取源文件夹和目标文件夹信息
    source_folder = "H:\\新建文件夹"
    target_root_folder = "H:\\测试"

    # 处理每一行数据
    overall_success_total = 0
    overall_failure_total = 0
    overall_failure_list_total = []

    for index, row in df.iterrows():
        success, failure, failure_list = process_row(source_folder, target_root_folder, row)
        overall_success_total += success
        overall_failure_total += failure
        overall_failure_list_total.extend(failure_list)

    print("\nSummary:")
    print(f"Total files copied successfully: {overall_success_total}")
    print(f"Total files failed to copy: {overall_failure_total}")
    if overall_failure_list_total:
        print("Failed files list:")
        for failed_file in overall_failure_list_total:
            print(f"- {failed_file}")

if __name__ == "__main__":
    main()


# Python脚本实现下面功能：
# 1、有一个根文件夹abc，包含多层子文件夹，每个子文件夹中都可能包含一些文件夹，文件夹中有很多文件需要复制到一个新的根文件夹bcd（bcd文件夹与abc文件夹不同）中，；
# 2、需要复制文件夹的文件名信息保存在一个Excel文件夹中，名为"move_file.xlsx"，其第1列表示文件名（只有文件名，不包含完整路径），第2列到第4列为要复制到的目标文件夹的信息，其中第2列为bcd文件夹的子文件夹名称，第3列为第2列文件夹的子文件夹名称（如空，则直接复制到上一级文件夹中），第4列为第3列文件夹的子文件夹的名称（如空，则直接复制到上一级文件夹中）。
# 3、如果目标文件夹不存在，则需要创建。
# 4、请用pandas库进行Excel文件的操作

# 程序增加一些功能：对于move_file_specific.xlsx中的每一行所对应的文件，可能不止复制到一个位置。
# 举例来说，第2列到第4列为要复制到的目标文件夹的信息，其中第2列为bcd文件夹的子文件夹名称，第3列为第2列文件夹的子文件夹名称（如空，则直接复制到上一级文件夹中），第4列为第3列文件夹的子文件夹的名称（如空，则直接复制到上一级文件夹中）；后面每三列如果非空的话，处理方法类似，例如之后第5列到第7列为要复制到的目标文件夹的信息，第6列为第5列文件夹的子文件夹名称（如空，则直接复制到上一级文件夹中），第7列为第6列文件夹的子文件夹的名称（如空，则直接复制到上一级文件夹中）。


