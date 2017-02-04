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



def searchToken(query, indexer, scorer, positioner, fileArcs):
	result = ''
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
						tempRes2.append(tpRes)
		for tpRes in tempRes2:
			validTpRes = True
			inTpRes = 1
			while(validTpRes and inTpRes < len(tpRes)):
				if (float(tpRes[inTpRes][2])-float(tpRes[inTpRes-1][2])-float(tpRes[inTpRes-1][3]) <= 0.5):
					inTpRes += 1
				else:
					validTpRes = False
			if(validTpRes):
				tbeg = tpRes[0][2]
				dur = float(tpRes[len(tpRes)-1][2])+float(tpRes[len(tpRes)-1][3])-float(tbeg)
				score = 1
				for res in tpRes:	
					score *= float(res[5])
				#print query[0],tpRes[0][0],tpRes[0][2], tpRes[len(tpRes)-1][2]
				pos0 = indexer[query[0]][tpRes[0][0]][tpRes[0][2]]['pos']
				posF = indexer[query[len(query)-1]][tpRes[0][0]][tpRes[len(tpRes)-1][2]]['pos']
				score *= reduce(lambda x, y: x*y, scorer[tpRes[0][0]][:pos0])
				score *= reduce(lambda x, y: x*y, scorer[tpRes[0][0]][posF:])
				result += '\n'
				result += '<kw file="' + tpRes[0][0] + '" channel="' + tpRes[0][1] + '" tbeg="' + str(tbeg) + '" dur="' + str(dur) + '" score="' + str(score)	+  '" decision="YES"/>'
		return result

#indexer['naendelea']['BABEL_OP2_202_15420_20140210_010333_inLine']['167.89']

def test():
	indexer, scorer, positioner, fileArcs = getIndexer('reference.ctm')
	query = ['naendelea', 'kungoja']	
	return searchToken(query, indexer, scorer, positioner, fileArcs)	

