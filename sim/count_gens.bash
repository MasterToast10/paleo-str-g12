#!/bin/bash


echo "generations, group" > r_prep.csv

for dir in */; do
    for sim in {1..30}; do
        echo "$(ls "$dir"sim_"$sim" | wc -l),${dir%/}" >> r_prep.csv
    done
done