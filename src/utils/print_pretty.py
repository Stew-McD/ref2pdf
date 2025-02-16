# print_pretty.py

from prettytable import PrettyTable, ALL
from config import DIR_PDF, DIR_FAIL, FILE_IN, FILE_OUT_BIB, FILE_OUT_CSV, FILE_LOG, DIRECT, UNPAYWALL, SCIHUB, SCRAPER, TIMEOUT, HEADERS


def print_config(df):
    
    settings_table = PrettyTable()
    settings_table1 = PrettyTable()
    # settings_table.set_style('ROUNDED') 

    settings_table.field_names = ["Setting", "Value"]
    settings_table.add_row(["INPUT FILE", FILE_IN])
    settings_table.add_row(["# TITLES", df.shape[0]])
    settings_table.add_row(["OUTPUT DIR", DIR_PDF])
    settings_table1.field_names = ["DOWNLOAD METHOD", "ON"]
    settings_table1.add_row(["DIRECT", DIRECT])
    settings_table1.add_row(["UNPAYWALL", UNPAYWALL])
    settings_table1.add_row(["SCIHUB", SCIHUB])
    settings_table1.add_row(["SCRAPER", SCRAPER])
    if SCRAPER:
        settings_table.add_row(["SOUP", True])
        settings_table.add_row(["SELENIUM", True])
        settings_table.add_row(["TIMEOUT", TIMEOUT])
        # settings_table.add_row({"HEADERS", HEADERS})


    print(f"\n{'='*62}\n")
    print("\t\t STARTING LITERATURE DOWNLOAD!")
    print(f"\n{'-'*62}\n")
    
    print("\n\t CONFIGURATION")
    print("-" * 62)
    print(settings_table)
    print(f"\n{'-'*62}\n")
    print(settings_table1)
    print(f"\n{'='*62}\n")
    
    
def print_results(df):
    
    # Create a table for the first section
    section1 = PrettyTable()
    # section1.set_style('ROUNDED')
    section1.field_names = ["Metric", "Value"]
    section1.add_row(["Total", df.shape[0]])
    section1.add_row(["Success", df[df['downloaded'] == 'success'].shape[0]])
    section1.add_row(["Failed", df[df['downloaded'] == 'failed'].shape[0]])

    # Create a table for the second section
    section2 = PrettyTable()
    # section2.set_style('ROUNDED')
    section2.field_names = ["Method", "Count"]
    section2.add_row(["Direct", DIRECT])
    section2.add_row(["Unpaywall", UNPAYWALL])
    section2.add_row(["SciHub", SCIHUB])
    section2.add_row(["Scraper", SCRAPER])

    # Create a table for the third section
    section3 = PrettyTable()
    # section3.set_style('ROUNDED')
    section3.field_names = ["Type", "Path"]
    section3.add_row(["Input file", FILE_IN])
    section3.add_row(["Output file", FILE_OUT_BIB])
    section3.add_row(["Output file", FILE_OUT_CSV])
    section3.add_row(["Log file", FILE_LOG])
    section3.add_row(["PDF directory", DIR_PDF])
    section3.add_row(["Failed directory", DIR_FAIL])

# make a table to print the failed downloads

# Set the maximum width for columns to enable text wrapping
    # section4 = PrettyTable()
    # section4.max_width["Title"] = 60  # Adjust the value to your desired width
    # section4.max_width["DOI"] = 32    # Adjust the value to your desired width
    # section4.max_width["URL"] = 60    # Adjust the value to your desired width
    # # section4.set_style('ROUNDED')
    # section4.field_names = ["Title", "DOI", "URL"]
    # for idx, row in df.iterrows():
    #     if row.downloaded == "failed":
    #         section4.add_row([row.title, row.doi, row.url])
            
    # Print the tables with decorative headers
    print("\n===== Finished literature download =====")
    print("-" * 32)
    print("\t RESULTS")    
    print(section1)
    print("-" * 32)
    print("\t DOWNLOAD METHOD")
    print(section2)
    print("-" * 32)
    print('\tFILES')
    print(section3)
    print("-" * 32)
    
    # SEE_FAILED = input('Do you want to print the failed downloads? (y/n): ')
    # if SEE_FAILED == 'y':
    #     section4.align["Title"] = "l"
    #     section4.align["DOI"] = "l"
    #     section4.align["URL"] = "l"
    #     section4.hrules = ALL
    #     print('\n\tFAILED DOWNLOADS')
    #     print(section4)
    #     print(f"\n{'='*32}\n")