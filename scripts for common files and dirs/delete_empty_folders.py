import os
from send2trash import send2trash

def delete_empty_folders(folder_path):
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if not os.listdir(dir_path):  # 判断文件夹是否为空
                # os.rmdir(dir_path)  # 删除空文件夹
                # print(f"已删除空文件夹: {dir_path}")
                send2trash(dir_path)
                print(f"已删除空文件夹并发送到回收站: {dir_path}")

def main():
    folder_path = r"F:\总备份\temp"
    delete_empty_folders(folder_path)

if __name__ == '__main__':
    main()

