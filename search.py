#!/usr/bin/env python

import docx
import PyPDF2
import os
import re
import sys
import argparse

"""
Class for obtaining summary of keywords found in a
folder of transcripts

Supports .pdf, .docx, and .txt file formats
"""
class KeywordSearch:
	
	def __init__(self, keyword_file, directories):
		"""
		Initialize KeywordSearch object

		Parameters
		----------
		directory: string
			Path of directory where documents are located
			Can be relative or absolute
		keyword_file: string
			Path of keyword file of Enter(newline)-separated
			words that are to be searched
		"""

		# Find transcripts in each directory, get keywords, and print findings
		self.transcripts = []
		for directory in directories:
			self.traverse_directory(curr_path=directory)
		self.load_keywords(keyword_file)
		print "Folders: {}\nKeywords: {}\nTranscripts: {}\n".format(", ".join(directories), ", ".join(self.keywords), ", ".join(self.transcripts))

	def traverse_directory(self, curr_path="."):
		"""
		Traverse a directory to find all files

		parameters
		----------
		curr_path: string
			Current file path of the recursive call

		returns
		-------
		No return value
		"""
		try:
			for item in os.listdir(curr_path):
				path = os.path.join(curr_path, item)
				if os.path.isdir(item):
					self.traverse_directory(curr_path=path)
				else:
					self.transcripts.append(path)
		except Exception as e:
			print "Error opening '{}'...".format(path)
			print e

	def load_keywords(self, keyword_file):
		"""
		Open and parse keyword file

		parameters
		----------
		keyword_file: string
			Path of the keyword file

		returns
		-------
		No return value
		"""
		try:
			with open(keyword_file, "r") as f:
				text = f.read().splitlines()
				self.keywords = [line for line in text if line]
		except Exception as e:
			print e
			exit(1)

	def parse(self):
		""" 
		Parse all transcripts for keywords
		"""
		for transcript in self.transcripts:

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

			# Print file information
			print "Searching through '{}'...".format(transcript)
			sys.stdout.write("File: {}\nKeywords:\n".format(transcript))

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
	"""
	Driver Code
	"""
	parser = argparse.ArgumentParser(description='Obtain summary information on keywords in transcripts (.docx, .pdf, .txt)')
	parser.add_argument('keyword_file', type=str, help='Path of keyword file of Enter(newline)-separated words that are to be searched')
	parser.add_argument('directories', type=str, nargs="+", help='Path of directory where documents are located. Can be relative or absolute')
	args = parser.parse_args()

	k = KeywordSearch(args.keyword_file, args.directories)
	k.parse()
