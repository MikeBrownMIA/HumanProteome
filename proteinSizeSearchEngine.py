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

#Define re pattern to extract protein name only from extraneous protein info
namePattern = r'\s[a-zA-Z][^A-Z]*[^=]+'

#Define Class and Functions
class protein:

	def __init__(self):

		self.proteinName = ''
		self.sequence = ''
		self.sequencelength = 0
		self.geneSymbol = ''
		self.estimatedSize = 0

	def getName(self, instance):
		name = re.search(namePattern, instance)
		proteinName = name.group()
		self.proteinName = proteinName[1:-3]

	def getGeneSymbol(self, instance):
		infoLst = instance.split('=')
		Symbol = infoLst[3]
		self.geneSymbol = Symbol[0:-3]

	def calculateLength(self):
		self.sequencelength = len(self.sequence)

	def estimateSize(self):
		self.estimatedSize = self.sequencelength * 0.110

species = "sapiens"
dataDict = {}
#counter to create unique key for dictionary
i = 0
currentKey = None
for line in proteomeList:
	#Use species as line identifier so that proteomes for other species can be run without changing loop
	if species in line:
		i += 1
		proteinInstance = protein()
		proteinInstance.getName(line)
		proteinInstance.getGeneSymbol(line)
		currentKey = (i, proteinInstance.geneSymbol)
		dataDict[currentKey] = proteinInstance

	else:
		#if line contains sequence data, add sequence to the current class instance and calculate the length
		dataDict[currentKey].sequence = line
		dataDict[currentKey].calculateLength()
		dataDict[currentKey].estimateSize()

# create a new dictionary where the keys consist of a tuple of the sequence length and protein name
keys = sorted(dataDict)
rankedDict = {}
for key in keys:
	proteinInstance = dataDict[key]
	newKey = (proteinInstance.estimatedSize, proteinInstance.proteinName, proteinInstance.geneSymbol)
	rankedDict[newKey] = proteinInstance

rankedDict = sorted(rankedDict)
# Ask user to search for protein and return results, do this until user enters 'quit'

while True:
	print("\nEnter the gene symbol or a keyword for the name of your protein(s) of interest to find its size in kDa:\n")
	print("Enter 'quit' to exit search engine at any time\n")
	userSearch = input()
	searchResultCounter = 0
	resultList = []
	for key in rankedDict:
		try:
			#Check if there is an exact match for the gene symbol
			if userSearch.lower() == key[2].lower():
				resultList = []
				searchResultCounter = 1
				print("\n{} - {} ({}) is approximately {} kDa.".format(searchResultCounter, key[1], key[2], '{:.1f}'.format(key[0])))
				break
			else:
				#Code will intentionally fail to push code to except statement
				searchResultCounter = key[1] % key[2]
			#If no exact matches, return all matches containing search criteria
		except:
			if userSearch.lower() in key[1].lower() or userSearch.lower() in key[2].lower():
				searchResultCounter += 1
				result = (key[0], key[1], key[2])
				resultList.append(result)
		
			elif userSearch.lower() == 'quit':
				sys.exit()

	else:
		if searchResultCounter == 0:
			print("\nNo search results found for:", userSearch)
		else:
			searchResultCounter = 0
			for key in resultList:
				searchResultCounter += 1
				print("\n{} - {} ({}) is approximately {} kDa.".format(searchResultCounter, key[1], key[2], '{:.1f}'.format(key[0])))
			print("\n", "Your search returned", searchResultCounter, "protein(s).")
		
