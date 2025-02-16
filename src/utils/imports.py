import pandas as pd
import bibtexparser
from bibtexparser.bparser import BibTexParser
from config import logger

# Function to return a DataFrame from various input formats
def return_df(FILE_IN):
    supported_formats = ('.bib', '.csv', '.json', '.txt')
    
    if FILE_IN.suffix in supported_formats or isinstance(FILE_IN, (list, dict)):
        try:
            if FILE_IN.suffix == '.bib':
                return load_bib(FILE_IN)
            elif FILE_IN.suffix == '.csv':
                return pd.read_csv(FILE_IN)
            elif FILE_IN.suffix == '.json':
                return pd.read_json(FILE_IN)
            elif FILE_IN.suffix == '.txt':
                return pd.read_csv(FILE_IN, header=None, names=['doi'])
            elif isinstance(FILE_IN, dict):
                return pd.DataFrame.from_dict(FILE_IN)
            elif isinstance(FILE_IN, list):
                return pd.DataFrame(FILE_IN, columns=['doi'])
        except Exception as e:
            logger.error(f"Error loading data from {FILE_IN}: {e}")
    
    else:
        logger.error(f"Unsupported file format or data type for {FILE_IN}")
        logger.info(f"Supported formats: {', '.join(supported_formats)}")
        logger.info("If .bib, .csv, .json, or dict, there must be a column named 'doi'.")
        logger.info("If a list, the list is assumed to contain only DOIs.")
        return None

# Function to load a BibTeX file into a DataFrame
def load_bib(FILE_IN):
    class CustomParser(BibTexParser):
        def __init__(self):
            BibTexParser.__init__(self)
            self.ignore_nonstandard_types = False
    
    try:
        with open(FILE_IN, 'r') as bibtex_file:
            parser = CustomParser()
            bib_database = bibtexparser.load(bibtex_file, parser=parser)

        return pd.DataFrame(bib_database.entries)
    except Exception as e:
        logger.error(f"Error loading BibTeX file {FILE_IN}: {e}")
        return None
