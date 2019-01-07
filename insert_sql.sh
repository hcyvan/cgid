#!/usr/bin/env bash

set -eu

readonly city=V0110000
readonly week=20180903
readonly I_DIR=./tar
readonly TAR_FILE="${I_DIR}/${city}_${week}_detail.sql.tar.gz"
readonly GZ_GRID_FILE="${I_DIR}/${city}_grid.sql.gz"


#gunzip -c ${GZ_GRID_FILE} |docker exec -i local-postgis psql -U postgres -d postgres

tar tf  "$TAR_FILE" | while read line; do
    echo "tar xzOf ${TAR_FILE} ${line}|docker exec -i local-postgis psql -U postgres -d postgres"
    tar xzOf ${TAR_FILE} ${line}|docker exec -i local-postgis psql -U postgres -d postgres
done


