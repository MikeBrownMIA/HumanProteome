humanRefProteome = "UP000005640_9606.fasta.gz"
f = open(humanRefProteome, "r")
proteomeList = f.readlines()
f.close()

#import Regular General Expressions Module
import re
import sys

#Concatenate list items anywhere & is found (i.e. join together fragments of sequences into one continuous sequence)
proteomeList[:] = [''.join([line.strip('\n') if ">" not in line else line for line in proteomeList])]
proteomeString = str(proteomeList)

#Separate Protein Information from AA sequences in list
proteomeList[:] = re.split(r">sp|>tr|\\n", proteomeString)
del proteomeList[0]

#Define Class and Functions
class protein:

	def __init__(self):

		self.proteinName = ""
		self.sequence = ""
		self.sequencelength = 0

	def calculateLength(self):
		self.sequencelength = len(self.sequence)

#Define re pattern to extract protein name only from extraneous protein info
pattern = r'\s[a-zA-Z][^A-Z]*[^=]+'
proteinName = ""
species = "sapiens"
dataDict = {}
#counter to create unique key for dictionary
i = 0
currentKey = None
for line in proteomeList:
	#Use species as line identifier so that proteomes for other species can be run without changing loop
	if species in line:
		proteinName = re.search(pattern, line)
		if proteinName:
			#Extract protein name
			i += 1
			proteinName = proteinName.group()
			proteinName = proteinName[1:-3]
			#Create class instance for each protein and use counter to create unique key for dictionary
			proteinInstance = protein()
			proteinInstance.proteinName = proteinName
			currentKey = (i, proteinName)
			#Create/add to Dictionary
			dataDict[currentKey] = proteinInstance

	else:
		#if line contains sequence data, add sequence to the current class instance and calculate the length
		dataDict[currentKey].sequence = line
		dataDict[currentKey].calculateLength()

# create a new dictionary where the keys consist of a tuple of the sequence length and protein name
keys = sorted(dataDict)
rankedDict = {}
for key in keys:
	proteinInstance = dataDict[key]
	newKey = (proteinInstance.sequencelength, proteinInstance.proteinName)
	rankedDict[newKey] = proteinInstance

rankedDict = sorted(rankedDict)
# Ask user to search for protein and return results, do this until user enters 'quit'

while True:
	print("\nEnter a keyword from the name of your protein(s) of interest to get the amino acid length(s):\n")
	print("Enter 'quit' to exit search engine at any time\n")
	userSearch = input()
	searchResultCounter = 0
	for key in rankedDict:
		if userSearch.lower() in key[1].lower():
			searchResultCounter += 1
			print("\n", searchResultCounter,'-', key[1], "is", key[0], "amino acids in length")
		elif userSearch.lower() == 'quit':
			sys.exit()
	else:
		if searchResultCounter == 0:
			print("\nNo search results found for:", userSearch)
		else:
			print("\n", "Your search returned", searchResultCounter, "protein(s).")
		


