./scripts/score.sh output/reference1.xml scoring
./scripts/termselect.sh lib/terms/ivoov.map output/reference1.xml scoring all

#2 run KWS on word decoding hyp
python indexer.py --in decode.ctm --out decode1.xml
./scripts/score.sh output/decode1.xml scoring
./scripts/termselect.sh lib/terms/ivoov.map output/decode1.xml scoring all
