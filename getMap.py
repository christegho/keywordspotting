def getMap():
	indir = './lib/kws/queries.xml'
	text = open(indir).read()
	entries = text.split('</kwtext>\n  </kw>\n  <kw ')
	output = ''
	entries[0] = entries[0].split('>\n  <kw ')[1]
	entries[len(entries)-1] = entries[len(entries)-1].split('</kwtext>\n  </kw>\n</kwlist>')[0]
	one = 0
	two = 0
 	three = 0
	four = 0
	five = 0
	more = 0
	for entry in entries:
		entry = entry.split('">\n    <kwtext>')
		query = entry[1].split(' ')
		kwid = entry[0].split('="')[1].split('-')[1]
		if len(query) == 1:
			output += 'one '+kwid+ ' ' + str(one).zfill(4)	+ '\n'
			one += 1
		elif len(query) == 2:
			output += 'two '+kwid+ ' ' + str(two).zfill(4)	+ '\n'
			two += 1
		elif len(query) == 3:
			output += 'three '+kwid+ ' ' + str(three).zfill(4)+ '\n'	
			three += 1
		elif len(query) == 4:
			output += 'four '+kwid+ ' ' + str(four).zfill(4)+ '\n'	
			four += 1
		elif len(query) == 5:
			output += 'five '+kwid+ ' ' + str(five).zfill(4)+ '\n'	
			five += 1	
		else:
			output += 'more '+kwid+ ' ' + str(more).zfill(4)+ '\n'	
			more += 1
	print one, two, three, four, five, more
	text_file = open("length.map", "w")
	text_file.write(output)
	text_file.close()

if __name__ == '__main__':
	getMap()

