EMD=$1

cd pro_${EMD}
sed  '1,7d' structure_set_1/emd_${EMD}.star > structure_set_1/emd_${EMD}_m.star
python ../split_star.py structure_set_1/emd_${EMD}_m.star
rm structure_set_1/emd_${EMD}_m.star

ls structure_set_1/*_emd_${EMD}.mrc |wc -l
ls structure_set_1/*_emd_${EMD}.star |wc -l

cd ..
