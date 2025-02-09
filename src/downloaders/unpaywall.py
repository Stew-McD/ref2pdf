import requests

from downloaders.direct_download import direct_download
from config import UNPAYWALL_EMAIL


def download_from_unpaywall(doi, title, ID):
    response = requests.get(f"https://api.unpaywall.org/v2/{doi}?email={UNPAYWALL_EMAIL}", verify=False)
    data = response.json()
    best_oa_location = data.get('best_oa_location')
    if best_oa_location and best_oa_location.get('url_for_pdf'):
        pdf_url = best_oa_location['url_for_pdf']
        title = data.get('title', doi)  # Use DOI as the title if title is absent
        if direct_download(pdf_url, title, ID):
            return pdf_url  # Return the successful URL
    return None  # Return None if download failed