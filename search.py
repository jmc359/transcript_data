#!/usr/bin/env python

import docx
import PyPDF2
import os
import re
import sys

"""
Class for obtaining summary of keywords found in a
folder of transcripts

Supports PDF, DOCX, and TXT file formats
"""
class KeywordSearch:
	
	def __init__(self, directory, keyword_file):
		"""
		Parameters
		----------
		directory: string
			Path of directory where documents are located
			Can be relative or absolute
		keyword_file: string
			Path of keyword file of Enter(newline)-separated
			words that are to be searched
		"""

		# Find transcripts in directory
		try:
			self.transcripts = [os.path.join(directory, transcript) for transcript in os.listdir(directory)]
		except:
			print "Folder '{}' not found. Exiting...".format(directory)
			exit(1)

		# Open and parse keyword file
		try:
			with open(keyword_file, "r") as f:
				text = f.read().splitlines()
				self.keywords = [line for line in text if line]
		except:
			print "Keywords file '{}' not found. Exiting...".format(keyword_file)
			exit(1)

		print "Folder: {}\nKeywords: {}\nTranscripts: {}\n".format(directory, ", ".join(self.keywords), ", ".join(self.transcripts))

	def parse(self):

		for transcript in self.transcripts:
			
			# Print file information
			print "Searching through '{}'...".format(transcript)
			sys.stdout.write("File: {}\nKeywords:\n".format(transcript))

			# Open file based on format
			if transcript.endswith(".docx"):
				document = docx.Document(transcript)
				self.text = [paragraph.text.encode('utf-8') for paragraph in document.paragraphs]
			elif transcript.endswith(".pdf"):
				pdfFileObj = open(transcript, 'rb')
				pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
				numPages = pdfReader.numPages
				self.text = ""
				for page in range(numPages):
					self.text += pdfReader.getPage(page).extractText().encode("utf-8").strip()
				self.text = self.text.split("\n")
			elif transcript.endswith(".txt"):
				wholeFile = open(transcript, "r")
				self.text = wholeFile.read().splitlines()
			else:
				print "Skipping {}...".format(transcript)
				continue

			# Check for keywords
			for word in self.keywords:
				sys.stdout.write("\t{}: {}\n".format(word, str(len(re.findall(r"({})".format(word), "\n".join(self.text))))))
				for line in self.text:
					found = re.findall(r"({})".format(word), line)
					if len(found) > 0:
						sys.stdout.write("\t\tLine {}: {}\n".format(str(self.text.index(line)+1), line))
			print "Done searching through '{}'\n".format(transcript)
		print "Search complete!"

if __name__ == "__main__":
	if len(sys.argv) < 3: 
		print "Improper number of arguments! \nUsage: {} folder_name keyword_file.txt".format(argv[0])
		exit(1)

	k = KeywordSearch(sys.argv[1], sys.argv[2])
	k.parse()
