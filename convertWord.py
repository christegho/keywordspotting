indir = './output/' + 'morph.xml'
text = open(indir).read()
entries = text.split('</detected_kwlist>\n')
output = '<kwslist kwlist_filename="IARPA-babel202b-v1.0d_conv-dev.kwlist.xml" language="swahili" system_id="">\n<detected_kwlist '
entries[0] = '<detected_kwlist kwid="KW202-00001" oov_count="0" search_time="0.0">\n'

for entry in entries:
	if entry != '</kwslist>\n':
		hits = entry.split('>')
		if (len(hits) > 2):
			scores = []
			output += hits[0] + '>'
			for i in range(1,len(hits)-1):
				scores.append(float(hits[i].split('score="')[1].split('" decision')[0])**2)
			totalScore = sum(scores)
			for i in range(1,len(hits)-1):
				output += hits[i].split('score="')[0]+ 'score="' + str(scores[i-1]/totalScore) + '" decision="YES"/>'
			output += '</detected_kwlist>\n'
		else:
			output += entry + '</detected_kwlist>\n'

output+='</kwslist>\n'

text_file = open('./output/morph2.xml', "w")
text_file.write(output)
text_file.close()
