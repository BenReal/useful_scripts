import os
import logging
import time
import hashlib


def configure_logging(log_file_path):
    # Ensure the log directory exists
    log_dir = os.path.dirname(log_file_path)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Open the log file with the desired encoding using FileHandler
    file_handler = logging.FileHandler(log_file_path, mode='a', encoding='utf8')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the FileHandler to the root logger
    logging.getLogger('').addHandler(file_handler)
    logging.getLogger('').setLevel(logging.INFO)


def add_timestamp(filename):
    base_name, extension = os.path.splitext(filename)
    current_time_str = time.strftime("%Y%m%d_%H%M%S")
    return f"{base_name}_{current_time_str}{extension}"


def calculate_run_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        run_time = end_time - start_time
        print("程序运行时间：{}秒".format(run_time))
        return result
    return wrapper


def calculate_sha256(file_content):
    sha256_hash = hashlib.sha256(file_content).hexdigest()
    return sha256_hash




def calculate_md5(file_content):
    md5_hash = hashlib.md5(file_content).hexdigest()
    return md5_hash

# 对于函数 calculate_sha256(file_content) 和 calculate_md5(file_content)，参数 file_content可以有不同的表示形式。
# 常见的文件内容表示形式包括：
# 字符串：如果文件内容是以字符串形式表示的，可以直接将字符串传递给这两个函数，无需进行编码。例如：
# file_content = "This is the content of the file."
# sha256_hash = calculate_sha256(file_content)
# md5_hash = calculate_md5(file_content)
# ```
# 字节流或二进制数据：如果文件内容是以字节流或二进制数据形式表示的，可以将字节流直接传递给这两个函数。例如：
# file_content = b'\x54\x68\x69\x73\x20\x69\x73\x20\x74\x68\x65\x20\x63\x6f\x6e\x74\x65\x6e\x74\x20\x6f\x66\x20\x74\x68\x65\x20\x66\x69\x6c\x65\x2e'
# sha256_hash = calculate_sha256(file_content)
# md5_hash = calculate_md5(file_content)
# ```
# 无论是字符串还是字节流，这两个函数都会根据给定的哈希算法计算文件内容的哈希值，并返回以十六进制表示的哈希值。
