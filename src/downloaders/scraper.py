import os
import requests
import urllib.parse
from prettytable import PrettyTable, ALL
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from selenium.webdriver.chrome.options import Options
from chromedriver_autoinstaller import install as chromedriver_install


# chromedriver_install()
# Suppress only the single InsecureRequestWarning from urllib3
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from config import HEADERS, TIMEOUT, DIR_PDF, DIR_FAIL, DIR_ROOT, VERBOSE

from downloaders.direct_download import direct_download


# Function to find PDF URLs from a webpage

def find_pdf_url(url, title):
    
    if not title:
        title = url
    
    pdf_links = []
    # Create headless Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode

    os.chdir(DIR_PDF)
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(url)
        WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
        
        # Extract PDF links from the loaded page
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        pdf_links += [a.get('href') for a in soup.select('a') if a.get('href', '').lower().endswith(('pdf', 'PDF'))]
    except Exception as e:
        print(f"\t ** {url}: {str(e)[:50]}")
    finally:
        driver.quit()

    response = requests.get(url, headers=HEADERS, verify=False)
    soup = BeautifulSoup(response.content, 'lxml')
    pdf_links += [a.get('href') for a in soup.select('a') if a.get('href', '').lower().find('pdf') != -1]

    for href in pdf_links:
        if href.startswith('/'):
            base_url = '/'.join(url.split('/')[:3])
            pdf_url = base_url + href
        else:
            pdf_url = href
        
        if direct_download(pdf_url, title):
            print(f"Scraped from PDF URL at '{pdf_url}'")
            return pdf_url  # Return the successful URL
        
    safe_title = ''.join(e for e in title if e.isalnum() or e.isspace()).replace(' ', '_')
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(url)
        WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
        driver.get(url)
        driver.save_screenshot(f'{DIR_FAIL}/{safe_title}_screenshot.png')
        with open(f'{DIR_FAIL}/"{safe_title}_page.html"', "w", encoding="utf-8") as f:
            f.write(driver.page_source)
            f.close()
    except Exception as e:
        print(f"\t ** {url} : {str(e)[:50]}")
    finally:
        driver.quit()
        
    print(f"Could not find PDF URL at '{url}'")
    return None 