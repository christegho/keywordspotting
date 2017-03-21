
#combine with 2015 CTM files
comb_all2 comb_dec_decmorph_decgraph_sn_50 comb_dec_decmorph_sn_50 comb_dec_decmorph_3366 comb_all2_nonsn

for sys1 in morph2 word2 word-sys3
do
for combs in comb_all2 comb_dec_decmorph_decgraph_sn_50 comb_dec_decmorph_sn_50 comb_dec_decmorph_3366 comb_all2_nonsn
do
python combine.py --hits1 ${sys1}.xml --hits2 ${combs}.xml --alpha 0.5 --beta 0.5 --out comb_${sys1}_${combs}_50.xml
python combine.py --hits1 ${sys1}.xml --hits2 ${combs}.xml --alpha 0.33 --beta 0.66 --out comb_${sys1}_${combs}_3366.xml
python combine.py --hits1 ${sys1}.xml --hits2 ${combs}.xml --alpha 0.66 --beta 0.33 --out comb_${sys1}_${combs}_6633.xml
done
done

for comb in morph2 word2 word-sys3
do
echo ------------------------------------ >> combsn.txt
echo ${comb} >> combsn.txt
./scripts/score.sh output/${comb}.xml scoring >> combsn.txt
./scripts/termselect.sh lib/terms/ivoov.map output/${comb}.xml scoring all >> combsn.txt
./scripts/termselect.sh lib/terms/ivoov.map output/${comb}.xml scoring iv >> combsn.txt
./scripts/termselect.sh lib/terms/ivoov.map output/${comb}.xml scoring oov >> combsn.txt
done

for w in 50 3366 6633
do
for sys1 in morph2 word2 word-sys3
do
for combs in comb_all2 comb_dec_decmorph_decgraph_sn_50 comb_dec_decmorph_sn_50 comb_dec_decmorph_3366 comb_all2_nonsn
do
comb=comb_${sys1}_${combs}_${w}
echo ------------------------------------ >> combsn.txt
echo ${comb} >> combsn.txt
./scripts/score.sh output/${comb}.xml scoring >> combsn.txt
./scripts/termselect.sh lib/terms/ivoov.map output/${comb}.xml scoring all >> combsn.txt
./scripts/termselect.sh lib/terms/ivoov.map output/${comb}.xml scoring iv >> combsn.txt
./scripts/termselect.sh lib/terms/ivoov.map output/${comb}.xml scoring oov >> combsn.txt
done
done
done


for sys1 in morph2 word2 word-sys3
do
for combs in morph2 word2 word-sys3
do
if [ "${sys1}" != "${combs}" ]
then
python combine.py --hits1 ${sys1}.xml --hits2 ${combs}.xml --alpha 0.5 --beta 0.5 --out comb_${sys1}_${combs}_50.xml
python combine.py --hits1 ${sys1}.xml --hits2 ${combs}.xml --alpha 0.33 --beta 0.66 --out comb_${sys1}_${combs}_3366.xml
python combine.py --hits1 ${sys1}.xml --hits2 ${combs}.xml --alpha 0.66 --beta 0.33 --out comb_${sys1}_${combs}_6633.xml
fi
done
done


for w in 50 3366 6633
do
for sys1 in morph2 word2 word-sys3
do
for combs in morph2 word2 word-sys3
do
if [ "${sys1}" != "${combs}" ]
then
comb=comb_${sys1}_${combs}_${w}
echo ------------------------------------ >> combsn.txt
echo ${comb} >> combsn.txt
./scripts/score.sh output/${comb}.xml scoring >> combsn.txt
./scripts/termselect.sh lib/terms/ivoov.map output/${comb}.xml scoring all >> combsn.txt
./scripts/termselect.sh lib/terms/ivoov.map output/${comb}.xml scoring iv >> combsn.txt
./scripts/termselect.sh lib/terms/ivoov.map output/${comb}.xml scoring oov >> combsn.txt
fi
done
done
done
done





for sys1 in comb_word-sys3_comb_dec_decmorph_decgraph_sn_50_6633 comb_word2_comb_dec_decmorph_decgraph_sn_50_6633 comb_morph2_word2_3366
do
for combs in comb_word-sys3_comb_dec_decmorph_decgraph_sn_50_6633 comb_word2_comb_dec_decmorph_decgraph_sn_50_6633 comb_morph2_word2_3366
do
if [ "${sys1}" != "${combs}" ]
then
python combine.py --hits1 ${sys1}.xml --hits2 ${combs}.xml --alpha 0.5 --beta 0.5 --out comb_${sys1}_${combs}_50.xml
python combine.py --hits1 ${sys1}.xml --hits2 ${combs}.xml --alpha 0.33 --beta 0.66 --out comb_${sys1}_${combs}_3366.xml
python combine.py --hits1 ${sys1}.xml --hits2 ${combs}.xml --alpha 0.66 --beta 0.33 --out comb_${sys1}_${combs}_6633.xml
fi
done
done

for w in 50 3366 6633
do
for sys1 in comb_word-sys3_comb_dec_decmorph_decgraph_sn_50_6633 comb_word2_comb_dec_decmorph_decgraph_sn_50_6633 comb_morph2_word2_3366
do
for combs in comb_word-sys3_comb_dec_decmorph_decgraph_sn_50_6633 comb_word2_comb_dec_decmorph_decgraph_sn_50_6633 comb_morph2_word2_3366
do
if [ "${sys1}" != "${combs}" ]
then
comb=comb_${sys1}_${combs}_${w}
echo ------------------------------------ >> combsn.txt
echo ${comb} >> combsn.txt
./scripts/score.sh output/${comb}.xml scoring >> combsn.txt
./scripts/termselect.sh lib/terms/ivoov.map output/${comb}.xml scoring all >> combsn.txt
./scripts/termselect.sh lib/terms/ivoov.map output/${comb}.xml scoring iv >> combsn.txt
./scripts/termselect.sh lib/terms/ivoov.map output/${comb}.xml scoring oov >> combsn.txt
fi
done
done
done
done


