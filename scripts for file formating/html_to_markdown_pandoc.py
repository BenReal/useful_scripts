import os
import subprocess

def convert_markdown_to_docx(input_file, output_file):
    # Use double quotes to handle paths with spaces and special characters
    # Increase memory limit for Pandoc PDF engine
    command = f'pandoc "{input_file}" -o "{output_file}"'
    # command = f'pandoc "{input_file}" -o "{output_file}" --resource-path="{input_file}" --pdf-engine=xelatex'
    print(f"Running command: {command}")
    result = subprocess.run(command, shell=True)
    print(f"Command exit code: {result.returncode}")
    # print(f"Converted: {input_file} -> {output_file}")

def batch_convert_markdown_to_docx(input_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Count total number of Markdown files
    total_files = sum(file_name.endswith('.html') for _, _, files in os.walk(input_directory) for file_name in files)

    # Walk through the directory tree
    processed_files = 0
    for root, dirs, files in os.walk(input_directory):
        for file_name in files:
            if file_name.endswith('.html') or file_name.endswith(".htm"):
                input_file = os.path.join(root, file_name)
                
                # Generate the output file path in the output directory
                relative_path = os.path.relpath(input_file, input_directory)
                output_file = os.path.join(output_directory, os.path.splitext(relative_path)[0] + '.md')
                
                # Convert and print status
                convert_markdown_to_docx(input_file, output_file)

                # Update processed file count
                processed_files += 1
                print(f"Processed {processed_files} of {total_files} files")

if __name__ == "__main__":
    input_directory = r"H:\测试"
    output_directory = r"H:\测试"

    batch_convert_markdown_to_docx(input_directory, output_directory)


# 此脚本使用Pandoc工具批量将指定目录及其子目录下的Markdown文件转换为DOCX文件。

# 使用步骤：
# 安装Pandoc： 请确保您的系统中已安装Pandoc。如果尚未安装，请根据官方指南进行安装。

# 配置Python环境： 请确保您的系统中已安装Python，并且python和pip命令可用。

# 安装依赖： 在终端或命令提示符中运行以下命令，安装脚本所需的依赖项：

# bash
# Copy code
# pip install markdown2docx
# 编辑脚本： 将提供的Python脚本保存为一个文件（例如convert_markdown_to_docx.py）。在脚本中，修改以下变量：

# python
# Copy code
# input_directory = "your_input_directory_path"
# output_directory = "your_output_directory_path"
# 将your_input_directory_path替换为包含Markdown文件的目录的实际路径，并将your_output_directory_path替换为生成的DOCX文件的输出目录的实际路径。

# 运行脚本： 在终端或命令提示符中运行脚本：

# bash
# Copy code
# python convert_markdown_to_docx.py
# 脚本将遍历指定目录及其子目录，将Markdown文件转换为DOCX文件。

# 查看结果： 转换完成后，您将在指定的输出目录中找到生成的DOCX文件。

# 请注意：确保Markdown文件中引用的图片可通过URL访问，以便Pandoc能够正确下载并嵌入这些图片。如果图片是本地文件，请使用相对路径引用以确保正确的转换。


