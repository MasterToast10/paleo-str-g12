#!/bin/bash

for dir in */; do
    touch ${dir%/}_gencount.csv
    echo "Simulation, Generations" > ${dir%/}_gencount.csv
    for sim in {1..30}; do
        echo "$sim", $(ls "$dir"sim_"$sim" | wc -l) >> ${dir%/}_gencount.csv
    done
done