import argparse
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
				print arc
				scorer[arc[0]].append(float(arc[5]))
				positioner[arc[0]].append(arc[4].lower())
				fileArcs[arc[0]].append(arc)
			else:
				position += 1
				scorer[arc[0]].append(float(arc[5]))
				positioner[arc[0]].append(arc[4].lower())
				fileArcs[arc[0]].append(arc)
			if (not(arc[4].lower() in indexer)):
				indexer.update({arc[4].lower() : {}})
			if (not(arc[0] in indexer[arc[4].lower()])):
				indexer[arc[4].lower()].update({arc[0] : {}})
			indexer[arc[4].lower()][arc[0]].update({arc[2]:{'ch':arc[1], 'dur':arc[3], 'score':arc[5], 'pos': position}})
	return indexer, scorer, positioner, fileArcs

def getOutput(inFile, outFile, queriesFile, snpower):
	indexer, scorer, positioner, fileArcs = getIndexer(inFile)
	indir = './lib/kws/' + queriesFile
	text = open(indir).read()
	entries = text.split('</kwtext>\n  </kw>\n  <kw ')
	output = '<kwslist kwlist_filename="IARPA-babel202b-v1.0d_conv-dev.kwlist.xml" language="swahili" system_id="">'
	entries[0] = entries[0].split('>\n  <kw ')[1]
	entries[len(entries)-1] = entries[len(entries)-1].split('</kwtext>\n  </kw>\n</kwlist>')[0]
	for entry in entries:
		entry = entry.split('">\n    <kwtext>')
		query = entry[1].split(' ')
		kwid = entry[0].split('="')[1]
		print query, kwid
		output +='\n<detected_kwlist kwid="' + kwid + '" oov_count="0" search_time="0.0">'
		output += searchToken(query, indexer, scorer, positioner, fileArcs, snpower)
		output += '\n</detected_kwlist>'
	output += '\n</kwslist>'
	text_file = open("output/"+outFile, "w")
	text_file.write(output)
	text_file.close()

def searchToken(query, indexer, scorer, positioner, fileArcs, snpower):
	result = ''
	tempRes = []
	tempRes2 = []

	fileA = []
	channelA = []
	tbegA = []
	durA = []
	scoreA = []

	for indexWord in range(len(query)):
		if query[indexWord] in indexer:
			tempRes.append(indexer[query[indexWord]])
		else:
			return result

	if len(tempRes) < 2:
		for file in indexer[query[indexWord]]:
			for arc in indexer[query[indexWord]][file]:
				dur = indexer[query[indexWord]][file][arc]['dur']
				score = float(indexer[query[indexWord]][file][arc]['score'])
				pos0 = int(indexer[query[indexWord]][file][arc]['pos'])
				fileA.append(file)
				channelA.append(indexer[query[indexWord]][file][arc]['ch'])
				tbegA.append(arc)
				durA.append(dur)
				scoreA.append(score)
				#score *= reduce(lambda x, y: x*y, scorer[file][:pos0])
				#score *= reduce(lambda x, y: x*y, scorer[file][pos0:])
		scoreTotal = sum(i**snpower for i in scoreA)
		for hit in range(len(tbegA)):
			result += '\n'
			result += '<kw file="' + fileA[hit] + '" channel="' + channelA[hit] + '" tbeg="' + tbegA[hit] + '" dur="' + durA[hit] + '" score="' + str((scoreA[hit]**snpower)/scoreTotal)	+  '" decision="YES"/>'
		return result

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
						#print indexWord,position,file
						if position+indexWord < len(positioner[file]):
							if (query[indexWord] == positioner[file][position+indexWord]):
								indexWord += 1
							else:
								validPosition = False		
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
				score = 0
				for res in tpRes:	
					score += float(res[5])
				score = score / float(len(tpRes))
				#print query[0],tpRes[0][0],tpRes[0][2], tpRes[len(tpRes)-1][2]
				pos0 = indexer[query[0]][tpRes[0][0]][tpRes[0][2]]['pos']
				posF = indexer[query[len(query)-1]][tpRes[0][0]][tpRes[len(tpRes)-1][2]]['pos']
				#if pos0 != 0:
					#score *= reduce(lambda x, y: x*y, scorer[tpRes[0][0]][:pos0])
				#print posF, len(scorer[tpRes[0][0]]), tpRes[0][0]
				#if posF != len(scorer[tpRes[0][0]])-1:
					#score *= reduce(lambda x, y: x*y, scorer[tpRes[0][0]][posF:])
				fileA.append(tpRes[0][0])
				channelA.append(tpRes[0][1])
				tbegA.append(str(tbeg))
				durA.append(str(dur))
				scoreA.append(score)
		scoreTotal = sum(i**snpower for i in scoreA)
		for hit in range(len(tbegA)):
			result += '\n'
			result += '<kw file="' + fileA[hit] + '" channel="' + channelA[hit] + '" tbeg="' + tbegA[hit] + '" dur="' + durA[hit] + '" score="' + str((scoreA[hit]**snpower)/scoreTotal) +  '" decision="YES"/>'
		return result
#from indexer import *
#indexer['naendelea']['BABEL_OP2_202_15420_20140210_010333_inLine']['167.89']

def test():
	indexer, scorer, positioner, fileArcs = getIndexer('reference.ctm')
	query = ['elisa']	
	return searchToken(query, indexer, scorer, positioner, fileArcs)	


def main() :
    
    parser = argparse.ArgumentParser(description='KWS Indexer.')
    #parser.add_argument('--ta', dest='timalign', action='store', default=0.2,      help='timalign')
    parser.add_argument('--in', dest='inFile', action='store', required=True,
                        help='In File CTM')
    parser.add_argument('--out', dest='outFile', action='store', required=True,
                        help='Out File XML')
    parser.add_argument('--queries', dest='queriesFile', action='store', required=True,
                        help='Out File XML')
    parser.add_argument('--sn', dest='snpower', action='store', required=True,
                        help='Out File XML')
   
    args = parser.parse_args()
    getOutput(args.inFile, args.outFile, args.queriesFile, float(args.snpower))
    
    
if __name__ == '__main__':
    main()

