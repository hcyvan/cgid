#!/usr/bin/env bash

#cat ./data/V0110000_grid.sql |docker exec -i local-postgis psql -U postgres -d postgres
#cat ./data/V0110000_20180903_detail_1_9.sql |docker exec -i local-postgis psql -U postgres -d postgres



#tar czvf V011000_20180903_detail.sql.tar.gz V011000_20180903_detail.*.sql
#tar tvf ./V011000_20180903_detail.sql.tar.gz

#tar xzOf V011000_20180903_detail.sql.tar.gz V011000_20180903_detail_1_9.sql
#
#cat ./data/V0110000_20180903_detail_1_9.sql |docker exec -i local-postgis psql -U postgres -d postgres

#tar_file =

tar tOf ./data/test/test/V0110000_20180903_detail.sql.tar.gz | while read line; do
    echo "$line"
done
