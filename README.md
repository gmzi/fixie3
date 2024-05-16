# Dev notes

**these tasks, in this order:**

- There are exceptions on dividends table reading. Go to /projects/pymu and experiment on how
to extract data from dividend pdfs, for some reason they get parsed unevenly and break the dataframe. Perhaps the way to go is grab de RECT position from the page.find_text() method, and work up from there, in order to get a more stable fromatting of columns. Try all this on pymu, not here. 

