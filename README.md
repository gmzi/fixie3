# Dev notes

**these tasks, in this order:**

- Play around on table_extractor/dividend loop to get the ticker symbol. That regex must have some trick.
- Do some more testing, comparing results from both fixie and fixie3. I'm really surprised that fixie3 seems to be more reliable than
previous version. If everything continues good, remove java from local computer. Deprecate fixie quick action. 
- Try to implement a browser version. This version will run with pyscript, pyodide and a service worker. Reuse elements from projects/calculator. On click, a browser with a drag and drop would open, and on file drop will trigger logic. With pyodide installed it should work pretty well. Support both the quick action and the browser version. Don't sweat about the browser versoin, remember this is a personal tool. 
- Explore formatting in fidelity 1099s and in Schwab 1099s, so as to add suport for those ones too. The get_text() approach should make it relatively easy to migrate around different pdf formats. If tables have lines and graphic vectors, might be able to explore find_tables(), if not stick with text extraction and regex. So the form would be fixie-vanguard, fixie-fidelity, fixie-schwab, etc, according to how different extraction processes work. 
- Keep it awesome, experimental and happy. 