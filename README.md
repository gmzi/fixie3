## Dev notes

**these tasks, in this order:**

- Explore formatting in fidelity 1099s and in Schwab 1099s, so as to add suport for those ones too. The get_text() approach should make it relatively easy to migrate around different pdf formats. If tables have lines and graphic vectors, might be able to explore find_tables(), if not stick with text extraction and regex. So the form would be fixie-vanguard, fixie-fidelity, fixie-schwab, etc, according to how different extraction processes work. 
- Try to implement a browser version. This version will run with pyscript, pyodide and a service worker. Reuse elements from projects/calculator. On click, a browser with a drag and drop would open, and on file drop will trigger logic. With pyodide installed it should work pretty well. Support both the quick action and the browser version. Don't sweat about the browser versoin, remember this is a personal tool. Implementation details:
    - Create a Pyscript app, try to stick Fixie in a portable way (don’t get too hooked on this, do it only if it’s simple enough, the important tool is the local one for my personal use).
    - [pymu running on pyodide](https://pymupdf.readthedocs.io/en/latest/pyodide.html)
- Keep it awesome, experimental and happy. 

__Goals of this version:__
- Run fixie in the client, with no need for a local python installation nor setup. 
- Get rid of PyPDF2 dependency that need Java to be installed on local machine. 
- Make it super portable, work offline like a native app. 


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
