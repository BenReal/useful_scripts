import os
from docx2pdf import convert

def convert_folder_to_pdf(folder_path):
    total_files = 0
    converted_files = 0
    failed_files = []
    
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".docx"):
                total_files += 1
                docx_path = os.path.join(root, file)
                pdf_path = os.path.splitext(docx_path)[0] + ".pdf"
                
                try:
                    convert(docx_path, pdf_path)
                    converted_files += 1
                    print(f"Converted {docx_path} to {pdf_path}")
                except Exception as e:
                    failed_files.append(docx_path)
                    print(f"\nFailed to convert {docx_path}: {str(e)}")
    
    print("Conversion summary:")
    print(f"Total files: {total_files}")
    print(f"Converted files: {converted_files}")
    print(f"Failed files: {len(failed_files)}")
    print("Failed files list:")
    for failed_file in failed_files:
        print(failed_file)

# 使用示例
folder_path = "H:\《XXXX》《XXXX》2023年10月27日\研究成果——项目（已分类）"  # 替换为你的文件夹路径
convert_folder_to_pdf(folder_path)


# 本程序使用docx2pdf，由于未知原因，转换成功率比较低。程序运行中会调用office程序。


