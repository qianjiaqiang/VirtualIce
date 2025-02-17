EMDID=$1
Res=$2
echo $EMDID
echo $Res
#if [ -f emd_${EMDID}.mrc ]
#then
#    echo emd_${EMDID} "is existed"
#else
#    echo emd_${EMDID}
#fi
python3 virtualice.py -s emd_${EMDID}.mrc  -n 300 -r ${Res} -J -o simu_${EMDID}_2 -pm 2  -D "m" -ao "False" -c 14 
