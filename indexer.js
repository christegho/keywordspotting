def getIndexer(filename):
	indir = './lib/ctms/' + filename
	text = open(indir).read()
	entries = text.split('\n')
	indexer = {}
	scorer = {}
	positioner = {}
	position = 0
	fileArcs = {}
	for entry in entries:
		arc = entry.split(' ')
		if (len(arc) > 4):
			if (not(arc[0] in scorer)):
				scorer.update({arc[0] : []})
				positioner.update({arc[0] : []})
				fileArcs.update({arc[0] : []})
				position = 0
			else:
				position += 1
				scorer[arc[0]].append(float(arc[5]))
				positioner[arc[0]].append(arc[4])
				fileArcs[arc[0]].append(arc)
			if (not(arc[4] in indexer)):
				indexer.update({arc[4] : {}})
			if (not(arc[0] in indexer[arc[4]])):
				indexer[arc[4]].update({arc[0] : {}})
			indexer[arc[4]][arc[0]].update({arc[2]:{'ch':arc[1], 'dur':arc[3], 'score':arc[5], 'pos': position}})
	return indexer, scorer, positioner, fileArcs

indexer, scorer, positioner, fileArcs = getIndexer('reference.ctm')

def searchToken(query, indexer, positioner, fileArcs):
result = []
tempRes = []
tempRes2 = []

for indexWord in range(len(query)):
	if query[indexWord] in indexer:
		tempRes.append(indexer[query[indexWord]])
	else:
			print 'non'

if len(tempRes) < 2:
	print tempRes
else:
	for file in tempRes[0]:
		validFile = True
		wordI = 1
		while (wordI < len(tempRes) and validFile):
			if (file in tempRes[wordI]):
				wordI += 1
			else : 
				validFile = False
		if (validFile):
			positions = [i for i, j in enumerate(positioner[file]) if j == query[0]]
			for position in positions:
				indexWord = 1
				validPosition = True
				while(validPosition and indexWord < len(query)):
					if (query[indexWord] == positioner[file][position+indexWord]):
						indexWord += 1
					else:
						validPosition = False
				if (validPosition):
					tpRes = []
					for indexWord in range(len(query)):
						tpRes.append(fileArcs[file][position+indexWord])
				`	tempRes2.append(tpRes)
	for tpRes in tempRes2:
		validTpRes = True
		inTpRes = 0
`		while(validTpRes and inTpRes < len(tpRes)):
			if ()
		
			











for tbeg in tempRes[0][file]:
				validTbeg = True
				wordI = 1
				while (wordI < len(tempRes) and validTbeg):
					for tbeg1 in tempRes[wordI][file]:
						if (float(tbeg1) - float(tbeg) - float(tempRes[wordI-1][file]['dur']) <= 0.5):


def evaluateTbeg(tempRes, file, validTbegs, word):

for tbeg in tempRes[0][file]:
	wordI = 1
	if (wordI < len(tempRes)):
		for tbeg1 in tempRes[wordI][file]:
			if (float(tbeg1) - float(tbeg) - float(tempRes[wordI-1][file]['dur']) <= 0.5):
				validTbegs = evaluateTbeg(tempRes[1:])
				break;			

	else:
		validTbegs[word].append(tbeg)
		word -= 1
return True
			
			




		


