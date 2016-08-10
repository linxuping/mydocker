while [ 1 ]
do
    ret=`ps auxf | grep python | grep -v grep | wc -l`
    if [ $ret == "0" ] 
    then
        cd /mnt
        ./run.sh
    fi
    sleep 60
done

