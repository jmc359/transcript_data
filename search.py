#!/usr/bin/env python

import docx
import os
import re
from sys import argv

if len(argv) != 3: 
	print "Improper number of arguments! \nUsage: {} folder_name keyword_file.txt".format(argv[0])
	exit(1)

try:
	transcripts = [os.path.join(argv[1], transcript) for transcript in os.listdir(argv[1]) if transcript.endswith(".docx")]
except:
	print "Folder '{}' not found. Exiting...".format(argv[1])
	exit(1)

try:
	with open(argv[2], "r") as f:
		text = f.read().splitlines()
		keywords = [line for line in text if line]
except:
	print "Keywords file '{}' not found. Exiting...".format(argv[2])
	exit(1)

print "Folder: {}\nKeywords: {}\nTranscripts: {}\n".format(argv[1], ", ".join(keywords), ", ".join(transcripts))

with open("output.txt", "w+") as f:
	for transcript in transcripts:
		print "Searching through '{}'...".format(transcript)
		f.write("File: {}\nKeywords:\n".format(transcript))
		document = docx.Document(transcript)
		text = [paragraph.text.encode('utf-8') for paragraph in document.paragraphs]
		for word in keywords:
			f.write("\t{}: {}\n".format(word, str(len(re.findall(r"({})".format(word), "\n".join(text))))))
			for line in text:
				found = re.findall(r"({})".format(word), line)
				if len(found) > 0:
					f.write("\t\tLine {}: {}\n".format(str(text.index(line)+1), line))
		print "Done searching through '{}'\n".format(transcript)
print "Search complete!"
