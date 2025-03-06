EMDID=$1
Res=$2
PX=$3
echo $EMDID
echo $Res
echo $PX
#if [ -f emd_${EMDID}.mrc ]
#then
#    echo emd_${EMDID} "is existed"
#else
#    echo emd_${EMDID}
#fi
# generate not too much
python3 virtualice.py -s emd_${EMDID}.mrc  -n 2 -r ${Res} -J -a ${PX} -nl 1 -o mem_${EMDID} -pm 1  -aa n -D "m" -ao "False" -ado 2.0  -c 14 
#python3 virtualice.py -s emd_${EMDID}.mrc  -n 2 -r ${Res} -J -om preferred -pa [*,90,0] [*,0,0] -a ${PX} -o mem_${EMDID} -pm 1  -D "m" -ao "False" -c 14 #-nf 20
