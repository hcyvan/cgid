#!/usr/bin/env bash

set -e

DATA=./data

TAR_DIR="$DATA/tar"
CSV_DIR="$DATA/csv"
SQL_DIR="$DATA/sql"

clear() {
    ls $1|grep $2|xargs -i echo "$1/{}"|xargs rm -f

}
for line in $(find $TAR_DIR | grep _detail.sql.tar.gz); do
    tar=$(echo "$line" | awk -F / '{print $5}')
    city=$(echo "$tar" | awk -F _ '{print $1}')
    week=$(echo "$tar" | awk -F _ '{print $2}')
    clear "$CSV_DIR/$city" "$week"
    clear "$SQL_DIR/$city" "$week"
done
