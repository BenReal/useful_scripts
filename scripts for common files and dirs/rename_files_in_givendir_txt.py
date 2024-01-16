import os


# 获取当前目录
root_path = r"G:\专题：无人抢滩登陆作战\新建文件夹\重点"

with open("./config/names_old.txt", "r", encoding="utf8") as f_old:
    lines_old = f_old.readlines()
    old_names = [line.strip() for line in lines_old if line]
    # print(old_names)

with open("./config/names_new.txt", "r", encoding="utf8") as f_new:
    lines_new = f_new.readlines()
    new_names = [line.strip() for line in lines_new if line]
    # print(new_names)


def check_string_lists(old_names, new_names):
    # Check if the lists have the same length
    if len(old_names) != len(new_names):
        print("The two lists have different lengths.")
        return 0

    # Check if the last 4 characters of the corresponding strings in the two lists are the same
    for i in range(len(old_names)):
        if old_names[i][-4:] != new_names[i][-4:]:
            print(
                f"The strings at index {i} in the two lists have different last 4 characters.")
            return 0

    # Check if the first list has no duplicates
    if len(old_names) != len(set(old_names)):
        print("The first list contains duplicates.")
        return 0

    return 1


if check_string_lists(old_names, new_names):

    num_files = 0
    fail_files = 0
    # 遍历目录下的所有文件
    for root, dirs, files in os.walk(root_path):
        for filename in files:
            # 判断是否需要更改文件名
            if filename in old_names:
                try:
                    # 获取文件的绝对路径
                    src = os.path.join(root, filename)
                    # 获取新文件名
                    dst = os.path.join(
                        root, new_names[old_names.index(filename)])
                    # 更改文件名
                    os.rename(src, dst)
                    num_files += 1

                except:
                    print(f"无法重命名：{filename}")
                    fail_files += 1
                    continue
    print(f"完成重命名：{num_files}个文件")
    print(f"重命名失败：{fail_files}个文件")
