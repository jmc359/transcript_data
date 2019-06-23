# Transcript Keyword Search
Repo for searching through PDF, DOCX, and Word documents for keywords/regular expressions

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

`keyword_file` refers to the Enter separated text (.txt) file containing the desired keywords/regular expressions to be searched. 

`directories` refers to the foldera or directories storing the desired Word (.docx), PDF (.pdf), or text (.txt) documents