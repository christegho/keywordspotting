import argparse

def editDistance(s1, s2, costs):

    m=len(s1)+1
    n=len(s2)+1

    tbl = {}
    for i in range(m): tbl[i,0]=i
    for j in range(n): tbl[0,j]=j
    for i in range(1, m):
        for j in range(1, n):
	    if 'sil' in costs[s1[i-1]]:
	    	costSil = 1-costs[s1[i-1]]['sil']/costs[s1[i-1]]['totalcount']
	    else:
		costSil = 1
	    if s1[i-1] == s2[j-1] :
		cost = 0
	    else:
		if s2[j-1] in costs[s1[i-1]]:
			cost = 1-costs[s1[i-1]][s2[j-1]]/costs[s1[i-1]]['totalcount']
		else:
			cost = costSil
	    
            tbl[i,j] = min(tbl[i, j-1]+costSil, tbl[i-1, j]+costSil, tbl[i-1, j-1]+cost)

    return tbl[i,j]


def getCosts():
	indir = '/home/ct506/Desktop/kws/lib/kws/grapheme.map'
	text = open(indir).read()
	entries = text.split('\n')
	costs = {}
	for entry in entries:
		if (entry!=''):
			
			entry = entry.split(' ')
			hyp = entry[1]
			ref = entry[0]
			refcost = float(entry[2])
			if hyp not in costs:
				costs[hyp] = {}
				costs[hyp]['totalcount'] = 0
			costs[hyp][ref] = refcost
			costs[hyp]['totalcount'] += refcost
	return costs

def getIV(filename):
	indir = './lib/ctms/' + filename
	text = open(indir).read()
	entries = text.split('\n')
	iv = []
	for entry in entries:
		arc = entry.split(' ')
		if (len(arc) > 4):
			if (not(arc[4] in iv)):
				iv.append(arc[4].lower())
	return iv		

def transformQueries(iv, outFile, costs, queriesFile):
	oov = 0;
	indir = './lib/kws/' + queriesFile
	text = open(indir).read()
	entries = text.split('</kwtext>\n  </kw>\n  <kw ')
	output = '<kwlist ecf_filename="IARPA-babel202b-v1.0d_conv-dev.ecf.xml" language="swahili" encoding="UTF-8" compareNormalize="lowercase" version="202 IBM and BBN keywords">'
	entries[0] = entries[0].split('>\n  <kw ')[1]
	entries[len(entries)-1] = kwid='kwid="KW202-00091">\n    <kwtext>kazi ya ko'#entries[len(entries)-1].split('</kwtext>\n</kw>\n</kwlist>')[0]
	for entry in entries:
		
		entry = entry.split('">\n    <kwtext>')
		query = entry[1].split(' ')
		kwid = entry[0].split('="')[1]
		#print query, kwid
		output +='\n  <kw kwid="'+kwid+'">'
		output += '\n    <kwtext>'
		for word in range(len(query)):
			if (query[word] in iv):
				output += query[word]
			else:
				closestIV = getClosestIV(query[word], iv, costs)				
				output += closestIV
				oov+=1
				print query[word], closestIV
			if (word != len(query)-1):
				output += ' '		
		output +='</kwtext>'
		output += '\n  </kw>'

	output += '\n</kwslist>'
	print oov
	text_file = open('./lib/kws/' + outFile, "w")
	text_file.write(output)
	text_file.close()

def getClosestIV(word, iv, costs):
	costsOOV = []
	for wordIV in iv:
		costsOOV.append(editDistance(word.replace("'",""), wordIV.replace("'",""), costs))
	return iv[costsOOV.index(min(costsOOV))]

def main() :
    parser = argparse.ArgumentParser(description='KWS Indexer.')
    parser.add_argument('--in', dest='inFile', action='store', required=True,
                        help='In File XML')
    parser.add_argument('--out', dest='outFile', action='store', required=True,
                        help='Out File XML')
    parser.add_argument('--queries', dest='queries', action='store', required=True,
                        help='Out File XML')
   
    
    args = parser.parse_args()
    costs = getCosts()
    print 'Got costs'
    iv = getIV(args.inFile)
    print 'Got IV words'
    print editDistance('lol','pop', costs)
    transformQueries(iv, args.outFile, costs, args.queries)
    
    
    
if __name__ == '__main__':
    main()

