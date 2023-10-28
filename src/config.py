import logging
import shutil
import os
from pathlib import Path

# Get the root directory of the project
DIR_ROOT = Path(__file__).resolve().parents[1]

FILE_IN = 'bib_extended.txt'
VERBOSE = True
DELETE = False

# CHOICE OF DOWNLOAD METHODS
DIRECT = 1
UNPAYWALL = 1
SCIHUB = 1
SCRAPER = 0

# File paths and directories
DIR_DATA = DIR_ROOT / "data"

DIR_INPUT = DIR_DATA / "input"
DIR_OUTPUT = DIR_DATA / "output"

FILE_IN = DIR_INPUT / FILE_IN
DIR_BIB = DIR_OUTPUT / "bib"
DIR_PDF = DIR_OUTPUT / "pdf"
DIR_FAIL = DIR_OUTPUT / "failed_downloads"
DIR_TMP = DIR_OUTPUT / "tmp"
DIR_LOG = DIR_OUTPUT / "log"

FILE_OUT_BIB = DIR_BIB / (FILE_IN.stem + "_out.bib")
FILE_OUT_CSV = DIR_BIB / (FILE_IN.stem + "out.csv")  
FILE_LOG = DIR_LOG / "ref2pdf.log"


for directory in [DIR_DATA, DIR_INPUT, DIR_OUTPUT, DIR_BIB, DIR_PDF, DIR_FAIL, DIR_TMP, DIR_LOG]:
    if DELETE and directory != DIR_INPUT:
        shutil.rmtree(directory, ignore_errors=True)
    directory.mkdir(parents=True, exist_ok=True)

## SCI-HUB SETTINGS
SCIHUB_DOMAINS = ['org', 'ru', 'se', 'cc', 'ee']

## UNPAYWALL SETTINGS
UNPAYWALL_API_KEY = (os.environ.get('UNPAYWALL_API_KEY'), None)
UNPAYWALL_EMAIL = (os.environ.get('UNPAYWALL_EMAIL'), 'scm@pm.me')

    
## SCRAPER SETTINGS
# User-Agent header
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36',
}

# CHOICES ABOUT USING SELENIUM OR BEAUTIFUL SOUP
SOUP = True
SELENIUM = True
TIMEOUT = 60


# LOGGER SETTINGS

# Create a logger
logger = logging.getLogger(__name__)

# Ensure the log directory exists
log_dir = DIR_LOG
log_dir.mkdir(parents=True, exist_ok=True)

# Configure logging to write to a file
log_file = FILE_LOG
logging.basicConfig(filename=log_file, level=logging.DEBUG if VERBOSE else logging.INFO)

# Optionally, configure the log format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

