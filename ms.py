#!/usr/bin/env python

import docx
import os
import re
from sys import argv

assert len(argv) > 2, "Missing argument...\n Usage: {} folder_name keywords.txt".format(argv[0])

keywords = [] 
transcripts = []
local = os.listdir(argv[1])
for transcript in local:
	transcripts.append(os.path.join(argv[1], transcript))

with open(argv[2], "r") as f:
	for line in f.read().splitlines():
		if line:
			keywords.append(line)

with open("output.txt", "w+") as f:
	for transcript in transcripts:
		if transcript.endswith(".docx"):
			f.write("File: {}\nKeywords:\n".format(transcript))
			document = docx.Document(transcript)
			text = [paragraph.text.encode('utf-8') for paragraph in document.paragraphs]
			for word in keywords:
				f.write("\t{}: {}\n".format(word, str(len(re.findall(r"({})".format(word), "\n".join(text))))))
				for line in text:
					found = re.findall(r"({})".format(word), line)
					if len(found) > 0:
						f.write("\t\tLine {}: {}\n".format(str(text.index(line)+1), line))
