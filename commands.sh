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
