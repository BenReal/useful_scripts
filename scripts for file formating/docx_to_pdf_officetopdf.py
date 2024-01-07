import os
import subprocess

def convert_docx_to_pdf(docx_path):
    pdf_path = os.path.splitext(docx_path)[0] + '.pdf'
    command = f'officetopdf "{docx_path}" "{pdf_path}"'

    print(f"Running command: {command}")
    result = subprocess.run(command, shell=True)
    print(f"Command exit code: {result.returncode}")

def convert_folder_files(folder_path):
    total_files = 0
    converted_files = 0
    failed_files = 0

    for foldername, subfolders, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename.endswith('.docx'):
                total_files += 1
                docx_path = os.path.join(foldername, filename)
                print(f"Converting file {total_files}: {docx_path}")
                try:
                    convert_docx_to_pdf(docx_path)
                    converted_files += 1
                except Exception as e:
                    failed_files += 1
                    print(f"Failed to convert {docx_path}: {str(e)}")
    
    print("Conversion summary:")
    print(f"Total files: {total_files}")
    print(f"Converted files: {converted_files}")
    print(f"Failed files: {failed_files}")

if __name__ == "__main__":
    folder_path = r'H:\《XXXX》《XXXX》2023年10月27日\研究成果——项目（已分类）'  # Replace this with the path to your folder
    convert_folder_files(folder_path)


# OfficeToPDF是一个命令行工具，可以将Microsoft Office文件转换为pdf格式。使用方法：下载officetopdf.exe文件，然后在命令行中运行officetopdf.exe，并提供两个参数：源Office文档和目标PDF文档。例如：officetopdf.exe input.docx output.pdf。


