#! /bin/sh

#for filename in $1*.log;do
#        rm $filename
#done
#for filename in $1*.ack;do
#        rm $filename
#done


#if [ -z "$(ls -A $1)" ]; then
#   echo "Empty"
#else
for filename in $1/*.dat;do
        echo "$filename"
        ./parser_edm80opc_live.py -f $filename -s $2
done
#fi
