# latex-dragoman
A small python application for automatic translation of LaTeX-text sections into other languages.

# Usage

To use this application, you'll need an API-Key for the free DeepL Pro API. Store this key in an env named "DEEPL_KEY" and the application should find it.

Run this application with `python3 src/createdocument.py <path-to-your-file> <abbreviation-of-target-language>`

After running, the application will output the merged document on your screen and also write it to `out/mergeddoc.tex`
Before running the application, please make sure there's no important documents still in `out/` since
`createdocument.py` will clear the directory before anything else when ran.
