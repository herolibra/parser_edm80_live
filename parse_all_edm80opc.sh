for folder in Data/SN19*;do
        echo $folder
        nohup sh parser_folder_edm80opc.sh $folder $1 &

done

