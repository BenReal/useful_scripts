import PyPDF2

# 定义PDF文件路径和要添加的元数据值
pdf_path = "6699.pdf"
metadata_field = "URL"
metadata_value = "https://www.jos.org.cn/jos/article/pdf/6699"

# 打开PDF文件
with open(pdf_path, "rb") as file:
    # 创建PDF阅读器对象
    pdf_reader = PyPDF2.PdfReader(file)
    
    # 获取第一页
    first_page = pdf_reader.pages[0]
    
    # 获取现有的元数据
    existing_metadata = pdf_reader.metadata.copy()
    
    # 添加新的元数据字段和值
    existing_metadata[metadata_field] = metadata_value
    
    # 创建PDF写入器对象
    pdf_writer = PyPDF2.PdfWriter()
    
    # 将现有页面添加到写入器
    pdf_writer.add_page(first_page)
    
    # 更新元数据
    pdf_writer.add_metadata(existing_metadata)
    
    # 保存到新的PDF文件
    output_path = "6699_with_metadata.pdf"
    with open(output_path, "wb") as output_file:
        pdf_writer.write(output_file)

print("已成功添加元数据字段到PDF文件：", output_path)
