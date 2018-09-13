# spreadsheet-images
Take lab reports or any papers with tables in them, and instantly extract those tables and convert them to Excel spreadsheets.
## Installation
1. Install OpenCV version > 3.0.
2. Install Tesseract OCR (used to recognize the text in the tables).
    - `sudo apt-get install tesseract-ocr libtesseract-dev libleptonica-dev`
    - `pip install pytesseract`
    - `pip install xlsxwriter`
    - `pip install pdf2image`
## Run
1. Run `make target=<filepath>` (or if `make` is not installed, then run `python main.py <filepath>`) on the command line where filepath is the path to the target image or PDF.

The resulting Excel spreadsheet should be in the `excel/`folder named `tables.xlsx`. Each table will have its own separate sheet when the file is opened.
