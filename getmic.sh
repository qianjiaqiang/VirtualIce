EMDID=$1
RES=$2
VOX=$3
PX=$4
echo -e "EMD $EMDID\t, RES $RES\t, VOX $VOX\t, PIXEL $PX"
#if [ -f emd_${EMDID}.mrc ]
#then
#    echo emd_${EMDID} "is existed"
#else
#    echo emd_${EMDID}
#fi
# generate not too much
python3 virtualice.py -s emd_${EMDID}.mrc  -n 300 -r ${RES} -J -a ${PX} -nl 1 -o pro_${EMDID} -pm 1  -aa n -D "m" -ao "False" -ado 1.6  -c 14 
#python3 virtualice.py -s emd_${EMDID}.mrc  -n 2 -r ${Res} -J -om preferred -pa [*,90,0] [*,0,0] -a ${PX} -o mem_${EMDID} -pm 1  -D "m" -ao "False" -c 14 #-nf 20
# test defocus
#python3 virtualice.py -s emd_${EMDID}_norm.mrc  -n 10 -r ${RES} -J -a ${PX} -nl 1 -o defocus_${EMDID}_norm -pm 1  -aa n -D "m" -ao "False" -ado 2.0  -c 14 
