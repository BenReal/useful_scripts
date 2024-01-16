import os
import sys
# 获取当前脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
# 如果当前目录是 'useful_scripts'，将当前目录加入搜索路径，否则，将父目录加入搜索路径
if os.path.basename(script_dir) == 'useful_scripts':
    sys.path.append(script_dir)
else:
    parent_dir = os.path.dirname(script_dir)
    sys.path.append(parent_dir)
# 导入其他模块
import shutil
import hashlib
import logging
import time
from local_modules.local_functions import configure_logging
from local_modules.local_functions import calculate_sha256


def move_file(src, dst):
    try:
        shutil.move(src, dst)
        return True
    except (shutil.Error, IOError, Exception) as e:
        logging.error(f"Error moving file '{src}' to '{dst}': {e}")
        
        # Handle name conflict by generating a new unique name for the source file
        base, ext = os.path.splitext(os.path.basename(src))
        new_name = f"{base}_DUPLICATE_{int(time.time())}{ext}"
        new_src = os.path.join(os.path.dirname(src), new_name)
        
        try:
            os.rename(src, new_src)
            shutil.move(new_src, dst)
            logging.info(f"File '{src}' moved to '{new_src}' due to a name conflict and then to '{dst}'.")
            return True
        except Exception as e:
            logging.error(f"Error moving file '{src}' to '{new_src}' and then to '{dst}': {e}")
            return False

def main():
    # Configure logging
    log_file_path = r'../logs/find_and_move_duplicate_shortfiles.log'
    configure_logging(log_file_path)

    # Record start time
    start_time = time.time()

    # Define source and destination folders
    src_dir = r"G:\专题：无人抢滩登陆作战"
    src_dir = os.path.normpath(src_dir)
    type_for_check = '.pdf'
    # type_for_check = '.txt'
    dst_dir = os.path.join(src_dir, '重复文件')

    # Create destination folder if it does not exist
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    # Define a dictionary to store file content and file paths
    file_dict = {}

    # Traverse all files in the source folder
    for root, dirs, files in os.walk(src_dir):
        if root == dst_dir:
            continue

        for file in files:
            if file.lower().endswith(type_for_check):
                file_path = os.path.join(root, file)                

                # Calculate file hash
                with open(file_path, 'rb') as f:
                    file_content = f.read()
                    len_file_content = len(file_content)
                    if len_file_content< 10:
                        print(f"文本长度：{len_file_content}，不进行比对：{file_path}")
                        continue
                    else:
                        file_hash = calculate_sha256(file_content)

                # Check if the hash value already exists in the dictionary
                if file_hash in file_dict:
                    existing_file_path = file_dict[file_hash]

                    # Compare file name lengths and move the shorter one
                    existing_file_len = len(os.path.basename(existing_file_path))
                    new_file_len = len(os.path.basename(file))

                    if existing_file_len < new_file_len:
                        logging.info(f"File '{existing_file_path}' is a duplicate of '{file_path}'. Moved '{existing_file_path}' to the destination folder.")
                        print(f"File '{existing_file_path}' is a duplicate of '{file_path}'. Moved '{existing_file_path}' to the destination folder.")
                        if not move_file(existing_file_path, dst_dir):
                            print(f"Failed to move file '{existing_file_path}' to the destination folder.")
                            continue
                        file_dict[file_hash] = file_path
                    else:
                        logging.info(f"File '{file_path}' is a duplicate of '{existing_file_path}'. Moved '{file_path}' to the destination folder.")
                        print(f"File '{file_path}' is a duplicate of '{existing_file_path}'. Moved '{file_path}' to the destination folder.")
                        if not move_file(file_path, dst_dir):
                            print(f"Failed to move file '{file_path}' to the destination folder.")
                            continue                       

                else:
                    file_dict[file_hash] = file_path

    # Record end time and calculate runtime
    end_time = time.time()
    run_time = end_time - start_time

    # Print runtime to console
    print("Program runtime: {} seconds".format(run_time))

    # Log runtime information
    logging.info("Program runtime: {} seconds".format(run_time))
    logging.info("Duplicate file check completed.")

    # Close the logging file
    logging.shutdown()

if __name__ == "__main__":
    main()


