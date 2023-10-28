from tqdm import tqdm
import shutil

# IMPORT CONFIGURATION
from config import DIR_TMP, FILE_IN, FILE_OUT_BIB, FILE_OUT_CSV
 
from utils import imports, exports, print_pretty
from downloaders import direct_download, unpaywall, scihub, scraper


def bib2pdf(file_bib):
    df = imports.return_df(FILE_IN)
    df['downloaded'] = 'not_attempted'
    df['downloaded_url'] = None
    
    print_pretty.print_config(df)
    progress_bar = tqdm(df.iterrows(), desc="Initializing...", total=df.shape[0])

    for idx, row in progress_bar:
        url = row.get('url', None)
        doi = row.get('doi', None)
        title = row.get('title', doi)

        progress_bar.set_description(f"Processing {title[:40]}...")

        if isinstance(url, str):
            success_url = direct_download.direct_download(url, title)
            if success_url:
                df = exports.update_dataframe(df, idx, 'success', success_url)
                print("   == Success: direct download")
                
                continue
        if doi:
            print(f"   --> unpaywall....")
            success_url =  unpaywall.download_from_unpaywall(doi, title)
            if success_url:
                df = exports.update_dataframe(df, idx, 'success', success_url)
                print("   == Success: unpaywall download")
                continue
        if doi:
            print(f"   --> scihub....")
            success_url = scihub.download_from_scihub(doi, title)
            if success_url:
                df = exports.update_dataframe(df, idx, 'success', success_url)
                print("   == Success: scihub download")
                continue
        if isinstance(url, str):
            try:
                success_url =  scraper.find_pdf_url(url, title)
            except Exception as e:
                print(f"\t ** Error finding PDF URL: {e}")            
            if success_url:
                df = exports.update_dataframe(df, idx, 'success', success_url)
                print("   == Success: webscraper download")
                continue
        df = exports.update_dataframe(df, idx, 'failed')
        print(" == Failed")

    print_pretty.print_results(df)

    exports.df_to_csv(df, FILE_OUT_CSV)
    exports.df_to_bibtex(df, FILE_OUT_BIB)
    
    return df

if __name__ == "__main__":

    df = bib2pdf(FILE_IN)
    shutil.rmtree(DIR_TMP, ignore_errors=True)
    