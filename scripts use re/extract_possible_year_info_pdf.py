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
import re
import logging
import time
from local_modules.local_functions import configure_logging
import pandas as pd
from io import StringIO
from pdfminer.high_level import extract_text
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter


def extract_text_from_pdf(pdf_path):
    try:
        # Using pdfminer.six to extract text content
        with open(pdf_path, 'rb') as pdf_file:
            resource_manager = PDFResourceManager()
            text_output = StringIO()
            device = TextConverter(resource_manager, text_output, laparams=None)
            interpreter = PDFPageInterpreter(resource_manager, device)
            
            for page in PDFPage.get_pages(pdf_file):
                interpreter.process_page(page)

            text = text_output.getvalue()
            text_output.close()

        return text
    except Exception as e:
        logging.error(f"Error extracting text from {pdf_path}: {str(e)}")
        return None


def process_pdf_file(pdf_path):
    try:
        # Extract PDF text content
        text = extract_text_from_pdf(pdf_path)

        # Initialize fields
        page_fields = {}

        # Iterate over each page
        for page_num, page_text in enumerate(re.split('\n\n', text)):
            # Generate page field names
            page_field_name_a = f'PAGE_{page_num + 1}A'
            page_field_name_b = f'PAGE_{page_num + 1}B'

            # Match year features
            page_fields[page_field_name_a] = '+'.join(re.findall(r'\b(?:19[5-9]\d|20\d{2})\b', page_text))
            page_fields[page_field_name_b] = '+'.join(re.findall(r'(19[5-9]\d|20\d{2})', page_text))

        # Fields TAIL_A and TAIL_B process the last page
        page_fields['TAIL_A'] = '+'.join(re.findall(r'\b(?:19[5-9]\d|20\d{2})\b', page_text))
        page_fields['TAIL_B'] = '+'.join(re.findall(r'(19[5-9]\d|20\d{2})', page_text))

        # Fields PAGE_1A_str, etc. process concatenated strings
        for page_num in range(1, 6):
            page_field_name = f'PAGE_{page_num}A'
            page_str_field_name = f'PAGE_{page_num}A_str'
            page_fields[page_str_field_name] = '+'.join(page_fields.get(page_field_name, '').split('+'))

        return {'File': pdf_path, **page_fields}
    except Exception as e:
        logging.error(f"Error processing file {pdf_path}: {str(e)}")
        return None


def process_directory(directory_path):
    result_list = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_path = os.path.join(root, file)
                result = process_pdf_file(pdf_path)
                if result:
                    result_list.append(result)
    return result_list

def main():
    # Configure logging with the desired encoding
    log_file_path = rr'../logs/extract_possible_year_info_pdf.log'
    configure_logging(log_file_path)

    start_time = time.time()

    # Specify the target directory
    target_directory = r'H:\新建文件夹'

    # Process pdf files in the specified directory
    results = process_directory(target_directory)

    # Save the results to an Excel file
    if results:
        df = pd.DataFrame(results)
        df.to_excel('output_result.xlsx', index=False)
        logging.info("Results saved to output_result.xlsx")
    else:
        logging.warning("No valid results to save.")

    end_time = time.time()
    run_time = end_time - start_time
    print("程序运行时间：{}秒".format(run_time))
    logging.info("程序运行时间：{}秒".format(run_time))

if __name__ == "__main__":
    main()
