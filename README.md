# spreadsheet-images
Take lab reports or any papers with tables in them, and instantly extract those tables and convert them to text files or Excel spreadsheets.
## Installation
1. Install OpenCV version > 3.0.
2. Install Tesseract OCR (used to recognize the text in the tables).
    - `sudo apt-get instsall tesseract-ocr libtesseract-dev libleptonica-dev`
    - `pip install tesserocr`
## Run
`python find_tables.py`

The images should be in the build/images folder. Note that you may need to clean the images before Tesseract can recognize them, so please run the textcleaner shell script with the images as input.
