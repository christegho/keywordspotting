indir = './output/' + 'word-sys2.xml'
text = open(indir).read()
entries = text.split('</detected_kwlist>\n')
output = '<kwslist kwlist_filename="IARPA-babel202b-v1.0d_conv-dev.kwlist.xml" language="swahili" system_id="">\n<detected_kwlist '
n = 1
for entry in entries:
	if entry != '</kwslist>\n':
		kwid = entry.split('kwid="')[1].split('" oov')[0]
		print kwid
		while (kwid[-3:]!=str(n).zfill(3)):
			output += '<detected_kwlist kwid="'+'KW202-00' + str(n).zfill(3)+'" oov_count="0" search_time="0.0">\n</detected_kwlist>\n'
			n+=1
		output += entry + '</detected_kwlist>\n'
		n+=1
output+='</kwslist>\n'

text_file = open('./output/word-sys3.xml', "w")
text_file.write(output)
text_file.close()
