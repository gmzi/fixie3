# Docs

This script processes a 1099 form in .pdf format, extracting data as text, parsing it to a pandas dataframe and exporting it to a a set of .csv files:
- `dividends.csv`. Displays data from the _Detail for Dividends and Distributions_ pages.
- `broker_transactions.csv`. Extracts data from the 1099-B section of the _Summary Information_ page ("Summary of Proceeds, Gains & Losses").
- `interest.csv`. Extracts data from section
And
- `sheets.xmls` is a single file combining the data described above into three worksheets.

## Usage
0. [Python](https://www.python.org/downloads/) is a required dependency.
1. Activate the virtual environment: `source venv/bin/activate`.
2. Install dependencies: `pip3 install -r requirements.txt`.
3. Create two empty folders in the main directory: `./input` and `./output`.
4. Place a 1099 file (in .pdf format) into the `./input` folder.
5. Run the program: `python3 test.py`.
6. Find the result files in the `./output` folder.

## Use as a Quick Action for Mac

To use this program as a Quick Action on a Mac:
- Create an Automator Quick Action that points to `./driver.sh` (instructions and an example script are provided in `./automator.sh`).
- Add your Quick Action to Finder on your Mac.
- Right-click any file in Finder; the Quick Action you created should be displayed under 'Quick Actions' (tested on Mac OS X Sonoma 14.1.1).

## Contribute
Please feel free to clone, fork, or contribute in any way you find interesting.

## Related

Resources and related topics worth to investigate IMO:
- This [blogpost](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/?utm_source=tldrwebdev) with links to these cool tools:
    - [ocr](https://tools.simonwillison.net/ocr)
    - [tesseract](https://github.com/tesseract-ocr/tesseract)
    - [PDF.js](https://mozilla.github.io/pdf.js/)
