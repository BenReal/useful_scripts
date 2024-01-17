import os

# 目录路径
directory = "G:\科研机构"

# 文件列表
file_list = [
"4—俄罗斯中央空气流体动力研究院（TsAGI）.docx", 
"18—法德圣路易斯研究所（ISL）.docx", 
"25—日本防卫装备厅（ATLA）.docx", 
"40—法国国家航空航天研究院（ONERA）.docx", 
]

# 创建文件
for file_name in file_list:
    file_path = os.path.join(directory, file_name)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w"):
        pass

print("文件创建完成！")
