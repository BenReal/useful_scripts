import os
import requests
import time
from fake_useragent import UserAgent  # You may need to install this library

def download_pdf_with_url(url, output_folder):
    headers = {'User-Agent': UserAgent().random}
    try:
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to download: {url}. Error: {e}")
        return

    # Extracting filename from URL
    filename = os.path.join(output_folder, f"{os.path.basename(url)}.pdf")

    with open(filename, 'wb') as pdf_file:
        for chunk in response.iter_content(chunk_size=128):
            pdf_file.write(chunk)

    print(f"Downloaded: {url}")
    time.sleep(2)  # Adding a delay to avoid being too aggressive with requests

if __name__ == "__main__":
    urls = [
        "https://eudl.eu/pdf/10.1007/978-3-319-76571-6_12",
        "https://www.worldscientific.com/doi/pdf/10.1142/S2737480723500085",
        "https://ceur-ws.org/Vol-2914/paper28.pdf",
        "https://link.springer.com/content/pdf/10.1007/s11432-022-3735-5.pdf"
    ]

    output_folder = "downloaded_pdfs"
    os.makedirs(output_folder, exist_ok=True)

    for url in urls:
        download_pdf_with_url(url, output_folder)
