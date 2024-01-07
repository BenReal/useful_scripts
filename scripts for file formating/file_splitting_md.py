import os
import re
from pathlib import Path


def process_markdown_files(input_directory, output_directory):
    for filename in os.listdir(input_directory):
        if filename.endswith(".md"):
            filepath = os.path.join(input_directory, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()

            # 获取文件名（不包括后缀）
            file_basename = os.path.splitext(filename)[0]

            # 使用正则表达式匹配一级标题
            pattern = re.compile(r'^(.+)\n==+$', flags=re.MULTILINE)
            matches = pattern.finditer(content)

            # 获取标题的起始位置
            start_positions = [match.start() for match in matches]
            start_positions.append(len(content))  # 添加末尾位置

            # 处理每个匹配项
            for i in range(len(start_positions) - 1):
                start_pos = start_positions[i]
                end_pos = start_positions[i + 1]

                # 获取原始中文数字标题
                old_heading_title = pattern.search(content, start_pos, end_pos).group(1).strip()

                # 替换文件名中的路径分隔符
                safe_heading_title = old_heading_title.replace(os.path.sep, '_').replace("/", "_")

                # 将中文数字替换为阿拉伯数字后接横杠
                new_heading_title = convert_chinese_number_to_arabic(safe_heading_title) + " -"

                # 构建新文件名
                new_filename = f"{file_basename}_{safe_heading_title}.md"

                # 构建新文件的完整路径
                new_filepath = os.path.join(output_directory, new_filename)

                # 写入新文件
                with open(new_filepath, 'w', encoding='utf-8') as new_file:
                    # 写入文件名和一级标题
                    new_file.write(f"# {file_basename} - {new_heading_title}\n\n")
                    # 写入剩余部分
                    new_file.write(content[start_pos:end_pos])


def convert_chinese_number_to_arabic(chinese_number):
    number_mapping = {"十一、": "11-", "十二、": "12-", "十三、": "13-", "十四、": "14-", "十五、": "15-", "十六、": "16-",
                      "十七、": "17-", "十八、": "18-", "十九、": "19-", "一、": "1-", "二、": "2-", "三、": "3-", "四、": "4-",
                      "五、": "5-", "六、": "6-", "七、": "7-", "八、": "8-", "九、": "9-", "十、": "10-", }
    for chinese, arabic in number_mapping.items():
        chinese_number = chinese_number.replace(chinese, arabic)
    return chinese_number


if __name__ == "__main__":
    # 替换为包含Markdown文件的目录的实际路径
    input_directory = r"G:\科研机构\科研机构MD（修改）"
    # 替换为保存结果的目录的实际路径
    output_directory = r"G:\科研机构\科研机构MD（分拆）"

    # 创建输出目录
    Path(output_directory).mkdir(parents=True, exist_ok=True)

    process_markdown_files(input_directory, output_directory)
