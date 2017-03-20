python indexer.py --in reference.ctm --out reference1.xml --queries queries.xml
./scripts/score.sh output/reference1.xml scoring
./scripts/termselect.sh lib/terms/ivoov.map output/reference1.xml scoring all

#2 run KWS on word decoding hypothesis
python indexer.py --in decode1.ctm --out decode1.xml --queries queries.xml
./scripts/score.sh output/decode1.xml scoring
./scripts/termselect.sh lib/terms/ivoov.map output/decode1.xml scoring all

#3 run KWS using output from a morphological decomposition.
#using morph.kwlist.dct
python transformToMorph.py --in morph.kwslist.dct --out  queries_morph_kwslist.xml
python indexer.py --in decode-morph.ctm --out decode_morph_kwslist.xml --queries queries_morph_kwslist.xml
./scripts/score.sh output/decode_morph_kwslist.xml scoring
./scripts/termselect.sh lib/terms/ivoov.map output/decode_morph_kwslist.xml scoring all

#using morph.dct
python CTMtoMorph.py --in morph.dct --out  decode1-morph.ctm
python indexer.py --in decode1-morph.ctm --out decode_morph.xml --queries queries_morph_kwslist.xml
./scripts/score.sh output/decode_morph.xml scoring
./scripts/termselect.sh lib/terms/ivoov.map output/decode_morph.xml scoring all
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

echo morph kwslist decode >> snresults.txt
python indexer.py --in decode-morph.ctm --out decode_morph_kwslist_${snpower}.xml --queries queries_morph_kwslist.xml --sn ${snpower}
./scripts/score.sh output/decode_morph_kwslist_${snpower}.xml scoring
./scripts/termselect.sh lib/terms/ivoov.map output/decode_morph_kwslist_${snpower}.xml scoring all >> snresults.txt
./scripts/termselect.sh lib/terms/ivoov.map output/decode_morph_kwslist_${snpower}.xml scoring iv >> snresults.txt
./scripts/termselect.sh lib/terms/ivoov.map output/decode_morph_kwslist_${snpower}.xml scoring oov >> snresults.txt
done


#Grapheme
snpower=2
python toGrapheme.py --in decode1.ctm --out queries-grapheme-decode.xml --queries queries.xml
python indexer.py --in decode1.ctm --out decode1_grapheme_${snpower}.xml --queries queries-grapheme-decode.xml --sn ${snpower}
./scripts/score.sh output/decode1_grapheme_${snpower}.xml scoring
./scripts/termselect.sh lib/terms/ivoov.map output/decode1_grapheme_${snpower}.xml scoring all 
./scripts/termselect.sh lib/terms/ivoov.map output/decode1_grapheme_${snpower}.xml scoring iv 
./scripts/termselect.sh lib/terms/ivoov.map output/decode1_grapheme_${snpower}.xml scoring oov 

python toGrapheme.py --in decode1.ctm --out queries-grapheme-decode.xml --queries queries.xml
python toGrapheme.py --in decode-morph.ctm --out queries-grapheme-morph.xml --queries queries_morph.xml
python toGrapheme.py --in decode-morph.ctm --out queries-grapheme-morph-kwslist.xml --queries queries_morph_kwslist.xml
for snpower in 0 1 2 3 
do
echo ------------------------------------
echo $snpower >> graphemeresults.txt
echo decode >> graphemeresults.txt
python indexer.py --in decode1.ctm --out decode1_grapheme_${snpower}.xml --queries queries-grapheme-decode.xml --sn ${snpower}
./scripts/score.sh output/decode1_grapheme_${snpower}.xml scoring
./scripts/termselect.sh lib/terms/ivoov.map output/decode1_grapheme_${snpower}.xml scoring all >> graphemeresults.txt
./scripts/termselect.sh lib/terms/ivoov.map output/decode1_grapheme_${snpower}.xml scoring iv >> graphemeresults.txt
./scripts/termselect.sh lib/terms/ivoov.map output/decode1_grapheme_${snpower}.xml scoring oov >> graphemeresults.txt

echo morph kwslist decode >> graphemeresults.txt
python indexer.py --in decode-morph.ctm --out decode_morph_kwslist_grapheme_${snpower}.xml --queries queries-grapheme-morph-kwslist.xml --sn ${snpower}
./scripts/score.sh output/decode_morph_kwslist_grapheme_${snpower}.xml scoring
./scripts/termselect.sh lib/terms/ivoov.map output/decode_morph_kwslist_grapheme_${snpower}.xml scoring all >> graphemeresults.txt
./scripts/termselect.sh lib/terms/ivoov.map output/decode_morph_kwslist_grapheme_${snpower}.xml scoring iv >> graphemeresults.txt
./scripts/termselect.sh lib/terms/ivoov.map output/decode_morph_kwslist_grapheme_${snpower}.xml scoring oov >> graphemeresults.txt
done

#System combination
#without score normalisation
python combine.py --hits1 decode1.xml --hits2 decode_morph_kwslist.xml --alpha 0.5 --beta 0.5 --out comb_dec_decmorph_50.xml
python combine.py --hits1 decode1.xml --hits2 decode_morph_kwslist.xml --alpha 0.33 --beta 0.33 --out comb_dec_decmorph_33.xml
python combine.py --hits1 decode1.xml --hits2 decode_morph_kwslist.xml --alpha 0.66 --beta 0.33 --out comb_dec_decmorph_6633.xml
python combine.py --hits1 decode1.xml --hits2 decode_morph_kwslist.xml --alpha 0.33 --beta 0.66 --out comb_dec_decmorph_3366.xml
python combine.py --hits1 decode1.xml --hits2 decode1_grapheme.xml --alpha 0.5 --beta 0.5 --out comb_dec_decgraph_50.xml
python combine.py --hits1 decode_morph_kwslist.xml --hits2 decode_morph_kwslist_grapheme.xml --alpha 0.5 --beta 0.5 --out comb_decmorph_decmorphgraph_50.xml

python combine.py --hits1 comb_dec_decmorph_50.xml --hits2 decode1_grapheme.xml --alpha 1 --beta 0.5 --out comb_dec_decmorph_decgraph_50.xml
python combine.py --hits1 comb_decmorph_decmorphgraph_50.xml --hits2 decode1_grapheme.xml --alpha 0.6 --beta 0.4 --out comb_all.xml

for comb in comb_dec_decmorph_decgraph_50 comb_dec_decmorph_50 comb_dec_decmorph_33 comb_dec_decmorph_6633 comb_dec_decmorph_3366 comb_dec_decgraph_50 comb_decmorph_decmorphgraph_50 comb_all
do
echo ------------------------------------ >> combresultsnonsn.txt
echo ${comb} >> combresultsnonsn.txt
./scripts/score.sh output/${comb}.xml scoring >> combresultsnonsn.txt
./scripts/termselect.sh lib/terms/ivoov.map output/${comb}.xml scoring all >> combresultsnonsn.txt
./scripts/termselect.sh lib/terms/ivoov.map output/${comb}.xml scoring iv >> combresultsnonsn.txt
./scripts/termselect.sh lib/terms/ivoov.map output/${comb}.xml scoring oov >> combresultsnonsn.txt
done

#with score normalisation
python combine.py --hits1 decode1_2.xml --hits2 decode_morph_kwslist_2.xml --alpha 0.5 --beta 0.5 --out comb_dec_decmorph_sn_50.xml
python combine.py --hits1 decode1_2.xml --hits2 decode_morph_kwslist_2.xml --alpha 0.33 --beta 0.33 --out comb_dec_decmorph_sn_33.xml
python combine.py --hits1 decode1_2.xml --hits2 decode_morph_kwslist_2.xml --alpha 0.66 --beta 0.33 --out comb_dec_decmorph_sn_6633.xml
python combine.py --hits1 decode1_2.xml --hits2 decode_morph_kwslist_2.xml --alpha 0.33 --beta 0.66 --out comb_dec_decmorph_sn_3366.xml
python combine.py --hits1 decode1_2.xml --hits2 decode1_grapheme_2.xml --alpha 0.5 --beta 0.5 --out comb_dec_decgraph_sn_50.xml
python combine.py --hits1 decode_morph_kwslist_2.xml --hits2 decode_morph_kwslist_grapheme_2.xml --alpha 0.5 --beta 0.5 --out comb_decmorph_decmorphgraph_sn_50.xml

python combine.py --hits1 comb_dec_decmorph_sn_50.xml --hits2 decode1_grapheme_2.xml --alpha 1 --beta 0.5 --out comb_dec_decmorph_decgraph_sn_50.xml
python combine.py --hits1 comb_dec_decmorph_sn_50.xml --hits2 decode1_grapheme_2.xml --alpha 0.5 --beta 1 --out comb_dec_decmorph_decgraph_sn_502.xml
python combine.py --hits1 comb_dec_decmorph_decgraph_sn_50.xml --hits2 decode_morph_kwslist_grapheme_2.xml --alpha 1.5 --beta 0.5 --out comb_all.xml
python combine.py --hits1 comb_dec_decmorph_decgraph_sn_50.xml --hits2 decode_morph_kwslist_grapheme_2.xml --alpha 0.5 --beta 1.5 --out comb_all2.xml

for comb in comb_dec_decmorph_decgraph_sn_502 #comb_dec_decmorph_sn_50 comb_dec_decmorph_sn_33 comb_dec_decmorph_sn_6633 comb_dec_decmorph_sn_3366 comb_dec_decgraph_sn_50 comb_decmorph_decmorphgraph_sn_50 comb_dec_decmorph_decgraph_sn_50 comb_all comb_all2
do
echo ------------------------------------ >> combresultssn.txt
echo ${comb} >> combresultssn.txt
./scripts/score.sh output/${comb}.xml scoring >> combresultssn.txt
./scripts/termselect.sh lib/terms/ivoov.map output/${comb}.xml scoring all >> combresultssn.txt
./scripts/termselect.sh lib/terms/ivoov.map output/${comb}.xml scoring iv >> combresultssn.txt
./scripts/termselect.sh lib/terms/ivoov.map output/${comb}.xml scoring oov >> combresultssn.txt
done
