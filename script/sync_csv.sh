#!/usr/bin/env bash

set -e
#./script/csv2sql.py sync-csv -i /home/xx/xx/xx/呼和浩特_徐州_常州_苏州_南通_201811 -o ./data

DIR="$1"

for dir1 in $(ls $DIR); do
    ABS_DIR1="$DIR/$dir1"
    for dir2 in $(ls $ABS_DIR1);do
        ABS_DIR2="$ABS_DIR1/$dir2"
        echo $ABS_DIR2
        ./script/csv2sql.py sync-csv -i "$ABS_DIR2" -o ./data
    done
done