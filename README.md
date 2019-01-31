# spreadsheet-images
Take lab reports or any papers with tables in them, and instantly extract those tables and convert them to Excel spreadsheets.

## Disclaimer
The textcleaner script was made by Fred Weinhaus. To use the textcleaner script in this repository for commercial use, redistribute it on the Internet, integrate it into free applications on the Internet, etc. you must contact Fred at fmw@alink.net for permission, or else you cannot use the textcleaner script. See the textcleaner file for more details. Users who use or fork this project have my permission to use and modify the rest of the code in this project, just not the textcleaner script. 

## Installation
1. Install Tesseract OCR (used to recognize the text in the tables).
    - `sudo apt-get install tesseract-ocr libtesseract-dev libleptonica-dev`
2. Install python libraries:
    - `pip install -r requirements.txt`
## Run
1. Run `make target=<filepath>` (or if `make` is not installed, then run `python main.py <filepath>`) on the command line where filepath is the path to the target image or PDF.

The resulting Excel spreadsheet should be in the `excel/`folder named `tables.xlsx`. Each table will have its own separate sheet when the file is opened.
