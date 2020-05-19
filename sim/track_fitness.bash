for dir in */; do
    echo "sim_id,generation,fitness" > "${dir%/}"_ftrack.csv
    for sim in {1..30}; do
        cnt=1
        while [ -f "$dir"sim_"$sim"/"$cnt".csv ]; do
            IFS="," read -a fields <<< $(sed -n 2p "$dir"sim_"$sim"/"$cnt".csv)
            echo "$sim","$cnt","${fields[1]}" | sed 's/ //g' >> "${dir%/}"_ftrack.csv
            cnt=$((cnt+1))
        done
    done
done
