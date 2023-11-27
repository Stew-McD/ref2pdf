import os
import wget
from time import sleep
from urllib.parse import urlparse

from config import DIR_PDF, DIR_ROOT, SLEEP, VERBOSE
from utils.file_checks import is_valid_pdf, make_safe_filename

BAR = None if VERBOSE else wget.bar_thermometer


# Function to download a PDF directly
def direct_download(url, title, ID):
    """
    use wget to download a PDF directly
    """

    sleep(SLEEP)
    os.chdir(DIR_ROOT)
    # Check if the URL is valid before attempting to download
    parsed_url = urlparse(url)
    if not parsed_url.scheme or not parsed_url.netloc:
        if VERBOSE:
            print(f"\t ** Invalid URL: {url}")
        return None

    # safe_title = make_safe_filename(title)
    safe_title = ID
    pdf_path = os.path.join(DIR_PDF, safe_title + ".pdf")
    if os.path.exists(pdf_path):
        print(f"\t ** File already exists: {pdf_path}")
        return
    if VERBOSE:
        print(f"\n Saving to: {pdf_path[:100]}")
    try:
        wget.download(url, out=pdf_path, bar=BAR)
        if is_valid_pdf(pdf_path):
            return url  # Return the successful URL
    except Exception as e:
        if VERBOSE:
            print(f"\t ** Error downloading {url}: {e}")
        pass
    return None  # Return None if download failed
