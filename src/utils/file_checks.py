import re
import os
import pdfplumber

from config import DIR_TMP, DIR_PDF

# Function to remove duplicates from a directory
def remove_duplicates(directory_path):
    pattern = re.compile(r'\s\(\d+\)\.\w+$')
    for file in os.listdir(directory_path):
        if pattern.search(file):
            filepath = os.path.join(directory_path, file)
            try:
                os.copy(filepath, DIR_TMP)
                # os.remove(file_path)
                print(f"\t ** Removed: {filepath}")
            except Exception as e:
                print(f"\t ** Error removing {filepath}: {e}")

# Function to check if a file is a valid PDF
def is_valid_pdf(filepath):
    try:
        with pdfplumber.open(filepath) as pdf:
            if len(pdf.pages) == 0:
                print(f"\t ** Empty PDF file: {filepath}")
                os.rename(filepath, os.path.join(DIR_TMP, os.path.basename(filepath)))
                return False

            first_page_text = pdf.pages[0].extract_text()
            if any(tag in first_page_text for tag in ['<html', '<body', '<head']):
                print(f"\t ** PDF contains HTML content: {filepath}")
                os.rename(filepath, os.path.join(DIR_TMP, os.path.basename(filepath)))
                return False

            return True
    except Exception as e:
        print(f"\t ** Not a valid PDF file: {filepath} : {e}")
        os.rename(filepath, os.path.join(DIR_TMP, os.path.basename(filepath)))
        return False

def make_safe_filename(title):
    # Replace any character that is not a letter, digit, space, or underscore with an empty string
    safe_title = re.sub(r'[^\w\s]', '', title)
    # Replace spaces with underscores
    safe_title = safe_title.replace(' ', '_')[:100]
    return safe_title


def pdf_exists(title):
    pdf_filename = os.path.join(DIR_PDF, make_safe_filename(title) + '.pdf')
    return os.path.exists(pdf_filename)