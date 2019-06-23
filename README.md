# Transcript Keyword Search
Repository for searching through .pdf, .docx, and .txt documents for keywords/regular expressions

## Setup
Make sure Python 2.7 is installed.
Then, in a terminal window:
```
pip install -r requirements.txt --user
```

## Usage
```
./search.py [-h] keyword_file directories [directories ...]
```

`keyword_file` refers to the Enter separated Text (.txt) file containing the desired keywords/regular expressions to be searched. 

`directories` refers to the folders or directories storing the desired Word (.docx), PDF (.pdf), or Text (.txt) documents