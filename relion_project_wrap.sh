EMD=$1
RES=$2
VOX=$3
PX=$4
if test -f emd_${EMD}.mrcs
then
    ls emd_${EMD}.mrcs
else
    #e2proc3d.py emd_${EMD}.mrc emd_${EMD}_norm.mrc --outtype=mrc --process=normalize.edgemean
    relion_project --i emd_${EMD}_norm.mrc --o emd_${EMD} --maxres ${RES} --angpix ${VOX} --ang rotate_181.star
    echo "project it" ${EMD}
fi
