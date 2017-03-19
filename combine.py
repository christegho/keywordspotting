import argparse
def combine(hitsFile1, hitsFile2, alpha, beta, outputFile):
	indir1 = './output/' + hitsFile1
	indir2 = './output/' + hitsFile2
	text1 = open(indir1).read()
	text2 = open(indir2).read()
	entries1 = text1.split('</detected_kwlist>\n')
	entries2 = text1.split('</detected_kwlist>\n')
	output = '<kwslist kwlist_filename="IARPA-babel202b-v1.0d_conv-dev.kwlist.xml" language="swahili" system_id="">\n'
	entries1[0] = entries1[0].split('<detected_kwlist ')[1]
	entries2[0] = entries2[0].split('<detected_kwlist ')[1]

	for index in range(1,len(entries1)):
		hits1 = entries1[index].split('\n<kw ')
		hits2 = entries2[index].split('\n<kw ')
		combinedHits = {}
		for indHit in range(1,len(hits1)):
			hitInfo = hits1[indHit].split(' ')
			print hitInfo
			tbeg = hitInfo[2].split('=')[1]
			file = hitInfo[0].split('=')[1]
			key = tbeg.split('"')[1]+file.split('"')[1]
			print key
			combinedHits[key] = {'file':file, 'dur':hitInfo[3].split('=')[1], 'score':1*float(hitInfo[4].split('="')[1].split('"')[0]), 'tbeg' : tbeg}
		
		for indHit in range(1,len(hits2)):
			hitInfo = hits2[indHit].split(' ')
			tbeg = hitInfo[2].split('=')[1]
			file = hitInfo[0].split('=')[1]
			key = tbeg.split('"')[1]+file.split('"')[1]
			#print key
			if key in combinedHits:
				combinedHits[key]['score'] = alpha*combinedHits[key]['score']+beta*float(hitInfo[4].split('="')[1].split('"')[0])
			else:
				combinedHits[key] = {'file':file, 'dur':hitInfo[3].split('=')[1], 'score':1*float(hitInfo[4].split('="')[1].split('"')[0]), 'tbeg': tbeg}
		if (len(hits1)>1 or len(hits2) >1):
			output += hits1[0]+'\n'
		else:
			output += hits1[0]
		print combinedHits
		for hit in combinedHits:
			output += '<kw file='+combinedHits[hit]['file']+' channel="1" tbeg=' + combinedHits[hit]['tbeg']+ ' dur=' + combinedHits[hit]['dur']+ ' score="'+str(combinedHits[hit]['score'])+'" decision="YES"/>\n'
		if (index != len(entries1)-1):
			output += '</detected_kwlist>\n'
	

	text_file = open('./output/' + outputFile, "w")
	text_file.write(output)
	text_file.close()


def main() :
    parser = argparse.ArgumentParser(description='KWS Indexer.')
    parser.add_argument('--hits1', dest='hits2', action='store', required=True,
                        help='In File XML')
    parser.add_argument('--hits2', dest='hits1', action='store', required=True,
                        help='Out File XML')
    parser.add_argument('--alpha', dest='alpha', action='store', required=True,
                        help='Out File XML')
    parser.add_argument('--beta', dest='beta', action='store', required=True,
                        help='Out File XML')
    parser.add_argument('--out', dest='out', action='store', required=True,
                        help='Out File XML')
   
    
    args = parser.parse_args()
    combine(args.hits1, args.hits2, float(args.alpha), float(args.beta), args.out)
    
if __name__ == '__main__':
    main()

