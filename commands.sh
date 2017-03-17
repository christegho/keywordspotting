python indexer.py --in reference.ctm --out reference1.xml --queries queries.xml
./scripts/score.sh output/reference1.xml scoring
./scripts/termselect.sh lib/terms/ivoov.map output/reference1.xml scoring all

#2 run KWS on word decoding hypothesis
python indexer.py --in decode1.ctm --out decode1.xml --queries queries.xml
./scripts/score.sh output/decode1.xml scoring
./scripts/termselect.sh lib/terms/ivoov.map output/decode1.xml scoring all

#3 run KWS using output from a morphological decomposition.
#using morph.dct
python transformToMorph.py --in morph.dct --out  queries_morph.xml
python indexer.py --in decode-morph.ctm --out decode_morph.xml --queries queries_morph.xml
./scripts/score.sh output/decode_morph.xml scoring
./scripts/termselect.sh lib/terms/ivoov.map output/decode_morph.xml scoring all

#using morph.kwlist.dct
python transformToMorph.py --in morph.kwslist.dct --out  queries_morph_kwslist.xml
python indexer.py --in decode-morph.ctm --out decode_morph_kwslist.xml --queries queries_morph_kwslist.xml
./scripts/score.sh output/decode_morph_kwslist.xml scoring
./scripts/termselect.sh lib/terms/ivoov.map output/decode_morph_kwslist.xml scoring all

#4

for snpower in 0 1 2 3 
do
echo ------------------------------------
echo $snpower >> snresults.txt
echo decode >> snresults.txt
python indexer.py --in decode1.ctm --out decode1_${snpower}.xml --queries queries.xml --sn ${snpower}
./scripts/score.sh output/decode1_${snpower}.xml scoring
./scripts/termselect.sh lib/terms/ivoov.map output/decode1_${snpower}.xml scoring all >> snresults.txt
./scripts/termselect.sh lib/terms/ivoov.map output/decode1_${snpower}.xml scoring iv >> snresults.txt
./scripts/termselect.sh lib/terms/ivoov.map output/decode1_${snpower}.xml scoring oov >> snresults.txt

echo morph decode >> snresults.txt
python indexer.py --in decode-morph.ctm --out decode_morph_${snpower}.xml --queries queries_morph.xml --sn ${snpower}
./scripts/score.sh output/decode_morph_${snpower}.xml scoring
./scripts/termselect.sh lib/terms/ivoov.map output/decode_morph_${snpower}.xml scoring all >> snresults.txt
./scripts/termselect.sh lib/terms/ivoov.map output/decode_morph_${snpower}.xml scoring iv >> snresults.txt
./scripts/termselect.sh lib/terms/ivoov.map output/decode_morph_${snpower}.xml scoring oov >> snresults.txt

echo morph kwslist decode >> snresults.txt
python indexer.py --in decode-morph.ctm --out decode_morph_kwslist_${snpower}.xml --queries queries_morph_kwslist.xml --sn ${snpower}
./scripts/score.sh output/decode_morph_kwslist_${snpower}.xml scoring
./scripts/termselect.sh lib/terms/ivoov.map output/decode_morph_kwslist_${snpower}.xml scoring all >> snresults.txt
./scripts/termselect.sh lib/terms/ivoov.map output/decode_morph_kwslist_${snpower}.xml scoring iv >> snresults.txt
./scripts/termselect.sh lib/terms/ivoov.map output/decode_morph_kwslist_${snpower}.xml scoring oov >> snresults.txt
done


#Grapheme
snpower=2
python toGrapheme.py --in decode1.ctm --out queries-grapheme-decode.xml
python indexer.py --in decode1.ctm --out decode1_grapheme_${snpower}.xml --queries queries-grapheme-decode.xml --sn ${snpower}
./scripts/score.sh output/decode1_grapheme_${snpower}.xml scoring
./scripts/termselect.sh lib/terms/ivoov.map output/decode1_grapheme_${snpower}.xml scoring all 
./scripts/termselect.sh lib/terms/ivoov.map output/decode1_grapheme_${snpower}.xml scoring iv 
./scripts/termselect.sh lib/terms/ivoov.map output/decode1_grapheme_${snpower}.xml scoring oov 
