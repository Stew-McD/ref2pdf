# ref2pdf

## Description

* Now with multiprocessing, it can download 1 paper per second approximately.

This Python package aims to automate the download of scientific papers from various sources including Unpaywall, Sci-Hub, and directly from publisher or other websites. It provides a flexible and extensible solution for obtaining papers in PDF format by using different strategies and methods.

The default is to use multiprocessing for the downloads, if that is not working, try the main_singleprocessing.py file.
If sci-hub domains are not working, go to the config.py file and change the sci-hub domains to those that are working right now.

Turn on and off deleting the output folder in the config.py file.

Also set the input and output files and folders there.

## What is not so good

* Scraping. It is a last resort, but for sure it could be improved to catch the papers that the other methods don't find.

## Features

* **Unpaywall Integration**: Downloads open-access papers from Unpaywall using their API. (unfortunately, not so good, maybe it can be improved with an API key, but they say that it is not necessary)
* **Sci-Hub Integration**: Attempts to get papers via Sci-Hub using multiple domain options.
* **Direct Scraping**: Downloads PDFs directly from webpages.
* **File Checks**: Validates if the downloaded PDFs are genuine and non-empty.

* You can turn on and off the different methods in the config.py file.

## Dependencies

* `requests`
* `pdfplumber`
* `beautifulsoup4`
* `selenium`
* `prettytable`
* `wget`
* `pandas`
* `bibtexparser`

## Example notebook

You can find an example notebook in the examples folder.


## Modules

### Imports

Responsible for loading a DataFrame from various input formats like `.bib`, `.csv`, `.json`, `.txt`, lists, and dictionaries.

### File Checks

Provides utility functions to validate PDF files and manage file duplicates.

### Direct Download

Contains a function for directly downloading PDF files from URLs.

### Sci-Hub

Manages the download process from Sci-Hub by using different domain options.

### Scraper

Scrapes web pages to find possible PDF URLs and then downloads them.

### Unpaywall

Downloads papers by communicating with the Unpaywall API.

## Installation

Just download the repository and run the main.py file.

## Usage

You can drop an input file in the input folder and run the main.py file. Also if you drop it in the root, it will work.
The input file can be a .bib, .csv, .json, .txt, or a list of DOIs. The output will be in the output folder.

## Contributing

Feel free to open issues or PRs if you have suggestions for improving this package.

## License

Unlicence
