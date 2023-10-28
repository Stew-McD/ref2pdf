import os
import wget
from urllib.parse import urlparse
from utils.file_checks import is_valid_pdf, make_safe_filename

from config import DIR_ROOT, DIR_PDF
# Function to download a PDF directly
def direct_download(url, title):
    os.chdir(DIR_ROOT)
    # Check if the URL is valid before attempting to download
    parsed_url = urlparse(url)
    if not parsed_url.scheme or not parsed_url.netloc:
        print(f"\t ** Invalid URL: {url}")
        return None
    
    safe_title = make_safe_filename(title)
    pdf_path = os.path.join(DIR_PDF, safe_title + '.pdf')
    print(f"Saving to: {pdf_path}") 
    try:
        wget.download(url, out=pdf_path)
        if is_valid_pdf(pdf_path):
            return url  # Return the successful URL
    except Exception as e:
        print(f"\t ** Error downloading {url}: {e}")
    
    return None  # Return None if download failed