import argparse

def getDict(dictFilename):
	indir = '/home/ct506/Desktop/kws/lib/dicts/' + dictFilename
	text = open(indir).read()
	entries = text.split('\n')
	dictMorph = {}
	for entry in entries:
		word = entry.split(' ')
		dictMorph[word[0]] = ' '.join(word[1:])
	return dictMorph

def transformQueries(dictMorph, outFile):
	oov = 0
	indir = './lib/ctms/' + 'decode1.ctm'
	text = open(indir).read()
	entries = text.split('\n')
	output = ''
	for entry in entries:
		if entry != '\n' and entry != '':
			entryS = entry.split(' ')
			#print entryS
			word = entryS[4]
			if (word in dictMorph):
				morph = dictMorph[word].split(' ')
				dur = float(entryS[3])/(len(morph))
				tbeg = float(entryS[2])
				for m in morph:
					output += entryS[0] + ' ' + entryS[1] + ' ' + str(tbeg) + ' ' + str(dur) + ' ' + m + ' '+entryS[5] + '\n'
					tbeg += dur
			else:
					output += entry + '\n'
					oov += 1
			
	print oov
	text_file = open('./lib/ctms/' + outFile, "w")
	text_file.write(output)
	text_file.close()



def main() :
    parser = argparse.ArgumentParser(description='KWS Indexer.')
    #parser.add_argument('--ta', dest='timalign', action='store', default=0.2,      help='timalign')
    parser.add_argument('--in', dest='dictFilename', action='store', required=True,
                        help='In File XML')
    parser.add_argument('--out', dest='outFile', action='store', required=True,
                        help='Out File XML')
   
    args = parser.parse_args()
    dictMorph = getDict(args.dictFilename)
    transformQueries(dictMorph, args.outFile)
    
if __name__ == '__main__':
    main()

