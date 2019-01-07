#!/usr/bin/env bash

set -eu

readonly city=V0110000
readonly week=20180903
readonly I_DIR=./data
readonly O_DIR=./tar

readonly SQL_FILES="${city}_${week}_detail_*.sql"
readonly TAR_FILE="${O_DIR}/${city}_${week}_detail.sql.tar.gz"

readonly GRID_FILE="${I_DIR}/${city}_grid.sql"
readonly GZ_GRID_FILE="${O_DIR}/${city}_grid.sql.gz"

target_file=""

for line in $(ls ${I_DIR}/${SQL_FILES}); do
    line_num=$(wc -l "$line"|awk '{print $1}')
    if [ $((line_num)) -gt 2 ]; then
        file_name=$(basename "$line")
        if [ "$target_file" == "" ]; then
            target_file="${file_name}"
        else
            target_file="${target_file} ${file_name}"
        fi
    fi
done

echo "gzip -c ${GRID_FILE} > ${GZ_GRID_FILE}"
gzip -c ${GRID_FILE} > ${GZ_GRID_FILE}

echo "tar czvf ${TAR_FILE} -C ${I_DIR} ${target_file}"
tar czvf ${TAR_FILE} -C ${I_DIR} ${target_file}


