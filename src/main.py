"""
|===============================================================|
| File: main.py                                                 |
| Project: ref2pdf                                              |
| Repository: www.github.com/Stew-McD/src                       |
| Description: Turn your bibliography into a pile of pdfs       |
|---------------------------------------------------------------|
| File Created: Friday, 27th October 2023 5:50:07 pm            |
| Author: Stewart Charles McDowall                              |
| Email: s.c.mcdowall@cml.leidenuniv.nl                         |
| Github: Stew-McD                                              |
| Company: CML, Leiden University                               |
|---------------------------------------------------------------|
| Last Modified: Saturday, 28th October 2023 11:45:22 pm        |
| Modified By: Stewart Charles McDowall                         |
| Email: s.c.mcdowall@cml.leidenuniv.nl                         |
|---------------------------------------------------------------|
|License: The Unlicense                                         |
|===============================================================|
"""

import concurrent.futures
from tqdm import tqdm

# IMPORT CONFIGURATION
# Import constants and configurations from the 'config' module.
from config import FILE_IN, FILE_OUT_BIB, FILE_OUT_CSV, DIRECT, UNPAYWALL, SCIHUB, SCRAPER

# Import utility modules
from utils import imports, exports, print_pretty

# Import downloaders
from downloaders import direct_download, unpaywall, scihub, scraper


# Function to process a single row of the DataFrame
def process_row(row):
    """
    Function to process a single row of the DataFrame.
    Called by bib2pdf_parallel() function.
    """
    url = row.url
    doi = row.doi
    title = row.title
    
    # Try direct download if URL is available
    if isinstance(url, str) and DIRECT:
        success_url = direct_download.direct_download(url, title)
        if success_url:
            return row.Index, "success", success_url

    # Try to download via Unpaywall if DOI is available
    if doi and UNPAYWALL:
        success_url = unpaywall.download_from_unpaywall(doi, title)
        if success_url:
            return row.Index, "success", success_url

    # Try to download via Sci-Hub if DOI is available
    if doi and SCIHUB:
        success_url = scihub.download_from_scihub(doi, title)
        if success_url:
            return row.Index, "success", success_url

    # Try scraping PDF from the webpage if URL is available
    if isinstance(url, str) and SCRAPER:
        try:
            success_url = scraper.find_pdf_url(url, title)
        except Exception as e:
            error = e
            # Error handling commented out
            pass
        if success_url:
            return row.Index, "success", success_url

    return row.Index, "failed", None


# Function to process the DataFrame and download the papers
def bib2pdf_parallel(FILE_IN):
    """
    Function to process the DataFrame and download the papers.
    Called by main() function.
    """
    df = imports.return_df(FILE_IN)
    df["downloaded"] = "not_attempted"
    df["downloaded_url"] = None

    total_tasks = df.shape[0]

    print_pretty.print_config(df)

    # Multi-threaded downloading of papers
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(
            tqdm(
                executor.map(process_row, df.itertuples()),
                total=total_tasks,
                desc="Processing Rows",
            )
        )

    # Update DataFrame based on download results
    for idx, status, success_url in results:
        if status == "success":
            df = exports.update_dataframe(df, idx, "success", success_url)
        else:
            df = exports.update_dataframe(df, idx, "failed")

    print_pretty.print_results(df)

    # Export results to CSV and BibTeX formats
    exports.df_to_csv(df, FILE_OUT_CSV)
    exports.df_to_bibtex(df, FILE_OUT_BIB)

    return df


# Entry point of the script
if __name__ == "__main__":
    df = bib2pdf_parallel(FILE_IN)
    # Cleanup temporary files (commented out)
    # shutil.rmtree(DIR_TMP, ignore_errors=True)
