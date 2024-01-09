import PyPDF2

def read_pdf_metadata(pdf_path):
    """
    Read metadata information from a PDF file.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        dict: Metadata information.
    """
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        metadata = pdf_reader.metadata
        return metadata

def read_pdf_headers_and_footers(pdf_path):
    """
    Read headers and footers information from each page of a PDF file.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        list: List of dictionaries containing page number, header, and footer information.
    """
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        headers_and_footers = []

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()

            # Extract headers and footers (assuming they are in the top and bottom 10% of the page)
            page_height = page.mediabox.height  # Use height instead of getHeight
            header_height = 0.1 * page_height
            footer_height = 0.1 * page_height

            header = page_text[:int(header_height)]
            footer = page_text[-int(footer_height):]

            # Append information to the list
            headers_and_footers.append({"Page": page_num + 1, "Header": header, "Footer": footer})

        return headers_and_footers


"""
PDF Analysis Script

This script analyzes a PDF file, extracting metadata and information about headers and footers on each page.

Usage:
    1. Update the 'pdf_path' variable with the path to the PDF file you want to analyze.
    2. Run the script using a Python interpreter.

Requirements:
    - Python 3.12 or later
    - PyPDF2 library
    - PyCryptodome library (for decryption, if applicable)

Usage Example:
    C:/Python312/python.exe h:/mycodes/sc1_for_tes.py

Output:
    - Metadata information including Author, Title, Subject, etc.
    - Headers and footers information for each page.

Note:
    - If you encounter the "DependencyError: PyCryptodome is required for AES algorithm" error,
      install the PyCryptodome library using 'pip install pycryptodome'.

    - Some methods used in the script may be deprecated in PyPDF2 version 3.0.0.
      Ensure you have an appropriate version of PyPDF2 installed (e.g., 1.26.0) to avoid issues.

    - The script may raise a DeprecationError related to PyPDF2 methods. In such cases, follow
      the suggested replacement in the comments.
"""
