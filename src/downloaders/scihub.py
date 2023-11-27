import requests
from bs4 import BeautifulSoup
import logging
import random
from time import sleep
from downloaders.direct_download import direct_download
from config import SCIHUB_DOMAINS, VERBOSE, SLEEP
from utils.file_checks import make_safe_filename

# Configure logging
logging.basicConfig(level=logging.DEBUG if VERBOSE else logging.INFO)
logger = logging.getLogger(__name__)


# Function to get PDF URL from Sci-Hub using DOI
def get_pdf_url_from_scihub(doi, domain):
    sleep(SLEEP)
    try:
        scihub_url = f"https://sci-hub.{domain}/{doi}"
        logger.debug(f"Sci-Hub URL (Domain: {domain}): {scihub_url}")
        response = requests.get(scihub_url, verify=False)
        soup = BeautifulSoup(response.content, "html.parser")
        embed_tag = soup.find("embed", id="pdf")
        if embed_tag:
            logger.debug(f"Embed tag: {embed_tag}")
            pdf_src = embed_tag["src"]
            logger.debug(f"PDF source URL: {pdf_src}")
            pdf_url = pdf_src if pdf_src.startswith("http") else f"https://{pdf_src}"
            logger.debug(f"PDF URL obtained from Sci-Hub (Domain: {domain}): {pdf_url}")
            return pdf_url
    except requests.exceptions.RequestException as e:
        logger.error(f"Error while fetching PDF URL from Sci-Hub (Domain: {domain}): {e}")

    return None


# Function to download PDF from Sci-Hub using DOI
def download_from_scihub(doi, title, ID):
    if not title:
        logger.debug(f"Title not provided for DOI: {doi}, using DOI as title")
        title = doi
    safe_title = make_safe_filename(title)
    logger.debug(f"Safe title for DOI: {doi}: {safe_title}")

    random.shuffle(SCIHUB_DOMAINS)
    for domain in SCIHUB_DOMAINS:
        try:
            pdf_url = get_pdf_url_from_scihub(doi, domain)
            logger.debug(f"Attempting to download from Sci-Hub using domain: {domain}")
            if pdf_url and direct_download(pdf_url, safe_title, ID):
                logger.info(f"Download successful from Sci-Hub using domain: {domain}")
                return pdf_url
        except Exception as e:
            logger.error(f"Error while downloading from Sci-Hub using domain: {domain}: {e}")

    return None
