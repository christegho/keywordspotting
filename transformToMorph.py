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
	indir = './lib/kws/' + 'queries.xml'
	text = open(indir).read()
	entries = text.split('</kwtext>\n  </kw>\n  <kw ')
	output = '<kwlist ecf_filename="IARPA-babel202b-v1.0d_conv-dev.ecf.xml" language="swahili" encoding="UTF-8" compareNormalize="lowercase" version="202 IBM and BBN keywords">'
	entries[0] = entries[0].split('>\n  <kw ')[1]
	entries[len(entries)-1] = entries[len(entries)-1].split('</kwtext>\n  </kw>\n</kwlist>')[0]
	for entry in entries:
		entry = entry.split('">\n    <kwtext>')
		query = entry[1].split(' ')
		kwid = entry[0].split('="')[1]
		#print query, kwid
		output +='\n  <kw kwid="'+kwid+'">'
		output += '\n    <kwtext>'
		for word in range(len(query)):
			if (query[word] in dictMorph):
				output += dictMorph[query[word]]
			else:
				output += query[word]
				oov += 1
				#print query[word]
			if (word != len(query)-1):
				output += ' '		
		output +='</kwtext>'
		output += '\n  </kw>'
	print oov
	output += '\n</kwslist>'
	text_file = open('./lib/kws/' + outFile, "w")
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

