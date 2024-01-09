import os
import pandas as pd
from tqdm import tqdm  # Optional: Provides a progress bar for the loop
from pathlib import Path
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

def process_directory(directory):
    """
    Process all PDF files in the given directory and its subdirectories.

    Args:
        directory (str): The root directory to start the traversal.

    Returns:
        pd.DataFrame: DataFrame containing metadata for each PDF file.
    """
    pdf_metadata_list = []

    for root, dirs, files in tqdm(os.walk(directory), desc="Processing PDFs", unit="file"):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_path = os.path.join(root, file)
                metadata = read_pdf_metadata(pdf_path)

                # Append filename to metadata
                metadata['Filename'] = file

                pdf_metadata_list.append(metadata)

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(pdf_metadata_list)

    # Reorder columns, placing 'Filename' first
    df = df[['Filename'] + [col for col in df.columns if col != 'Filename']]

    return df

def save_to_excel(dataframe, excel_path):
    """
    Save DataFrame to an Excel file.

    Args:
        dataframe (pd.DataFrame): The DataFrame to be saved.
        excel_path (str): The path to save the Excel file.
    """
    dataframe.to_excel(excel_path, index=False)

if __name__ == "__main__":
    # Set the root directory
    root_directory = r'H:\测试'

    # Set the output Excel file path
    excel_file_path = 'pdf_metadata.xlsx'

    # Process the directory and get metadata DataFrame
    metadata_df = process_directory(root_directory)

    # Save metadata DataFrame to Excel file
    save_to_excel(metadata_df, excel_file_path)

    print("Metadata extraction and Excel file creation completed.")
