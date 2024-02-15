# This script analyse the docs folder, which sort documents per year.
# For each document, 
# 	it identifies the country based on the "countries.md" file by looking at the metadata title, and the first page
# 	It counts the occurrences of a list of keywords, along with the most common words in the document excluding common words.
# It then produces a CSV document, 
# Xavier Lavayssière - December 2023

import os
import glob
import re
import pypdf
import pandas as pd
import csv
import os

class Style():
  RED = "\033[31m"
  GREEN = "\033[32m"
  YELLOW = "\033[33m"
  BLUE = "\033[34m"
  RESET = "\033[0m"

# Generic constansts
common_words = {"the", "be", "to", "of", "and", "a", "in", "that", "have", "I"}
months = {"January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"}
useless_title_words = {"Microsoft", "Word", "Information", "Supplementary", 'for', "No", 'Release', 'Statement', "And","Annex",  "Informational", 
'Consultation', 'and', 'director', 'Alternate', 'Iv', 'Executive', 'IV', 'Staff', 'Report;', 'IMF', 'Article', 'Report', 'No.', 'by', 'Consultation', 'Director', 'executive', 
'statement', 'Country', 'the', 'article', 'of', 'Press', 'consultation','Press', "Consulation",
"Stattement", "Supplement", "Republic"}
# Normalize useless_title_words
useless_title_words = {word.title() for word in useless_title_words}

# We create a list of countries from a file
# Careful look at name that belong to other countries' name : 
# Republic of Congo,  People's Republic of China, Aruba - netherlands
def load_countries(filename):
	countries = list()
	# 'with' can automate finish 'open' and 'close' file
	with open(filename) as f:
		# fetch one line each time, include '\n'
		for line in f:
			# strip '\n', then append it to countries
			countries.append(line.rstrip('\n'))
	return countries
  
# We give our best guess for the country name
# We use the list of countries and try to find a matching exact name in the firstpage
# otherwise in the metadata
# otherwise returns file name
def extractTitle(reader, file):
	# First page check
	firstpage = reader.pages[0].extract_text() # + reader.pages[1].extract_text()
	meta = reader.metadata
	for country in countries:
		subnames = country.split(",")
		# print(subnames, firstpage[:100])
		for subname in subnames:
			c = re.compile(r'\b'+re.escape(subname)+r'\b', re.IGNORECASE)
			m = re.search(c, firstpage[:300])
			if m:
				# print("Direct match", m)
				# if subname == "Belarus":
				# 		print("Belarus", m, firstpage)
				return subnames[0]
	print(f"{Style.RED}Country not fond in {Style.RESET}", firstpage[0:300])
	# Filename case
	if meta.title is None or len(meta.title.strip())<4:
		print(f"{Style.YELLOW} using file{Style.RESET}",file)
		return file + "(Filename)"
	# Metadata case
	for country in countries:
		subnames = country.split(",")
		for subname in subnames:
			c = re.compile(re.escape(subname), re.IGNORECASE)
			if re.search(c, meta.title):
				print(f"{Style.YELLOW} but found in {Style.RESET}", meta.title)
				return subnames[0]
	print(f"{Style.RED}   nor in {Style.RESET}", meta.title)
	# Default messy case
	titleList = re.split(r'\W+', meta.title)
	titleList = {word.title() for word in titleList}
	filtered_titleList = " ".join({word for word in titleList if word not in useless_title_words and not word.isdigit()and not word in months})
	print(f"{Style.YELLOW} using messy title{Style.RESET}", filtered_titleList)
	return filtered_titleList.strip() + "(Messy)"

# Returns a dictionary with the number of documents containing the keyword in the folder
def count_documents(keyword, folder_path, index, DasMetaTable):
	for root, dirs, files in os.walk(folder_path):
		dirname, folder = os.path.split(root)
		print("\n🗓", folder, keyword)
		for file in files:
			if file.endswith(".pdf"):
				file_path = os.path.join(root, file)
				with open(file_path, 'rb') as f:
					pdf_reader = pypdf.PdfReader(f)
					title = extractTitle(pdf_reader, file)
					# WHen adding a new country, it has -1 for all years
					if title not in DasMetaTable:
						DasMetaTable[title] = [-1 for i in range(len(years))]
						print("New country: ", title)
					# If the country has a document for the year, and no prior document (some years have two documents e.g. report and a summary) it is set to 0
					if DasMetaTable[title][index] == -1:
						DasMetaTable[title][index] = 0
					DasMetaTable[title][index] = 0
					content = ""
					for page in pdf_reader.pages:
						content += page.extract_text()
					m = re.findall(keyword, content)
					if m:
						DasMetaTable[title][index] += len(m)
						print(" ",title,"->", m)
	return DasMetaTable

# Write dictionary to CSV file
def dict_to_csv(dictionary, filename):
    keys = list(dictionary.keys())
    values = list(dictionary.values())

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(keys)
        writer.writerows(zip(*values))

if __name__ == "__main__":
	# Intialize variables

	countries = load_countries("countries.md")

	# To match "digitalizing", "digitalization", or "digitalize"
#	keyword = re.compile("digitaliz(e|ing|ation)"+r'\b', re.IGNORECASE)

# Digital
	keyword = re.compile("digital", re.IGNORECASE)


	years = [2016,2017,2018,2019,2020,2021,2022,2023]
	metaTable = {"Years": years}
	fldr = input("Enter a folder to analyze (must be within the current folder) ")
	root = os.path.join(os.getcwd(), fldr)

	# Run for each year
	for index, year in enumerate(years):
		folder_path = os.path.join(root, str(year))
		if os.path.isdir(folder_path):
			count_documents(keyword, folder_path, index, metaTable)

	# Convert dictionary to CSV
	print(metaTable)
nextOutput = 'output-'+fldr+'.csv'
if os.path.isfile(nextOutput):
	os.rename(nextOutput, 'output-'+fldr+'99.csv')
dict_to_csv(metaTable, nextOutput)
print('The converted CSV file is created successfully in the working directory ('+nextOutput+')')

