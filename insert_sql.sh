#!/usr/bin/env bash

#cat ./data/V0110000_grid.sql |docker exec -i local-postgis psql -U postgres -d postgres
cat ./data/V0110000_20180903_detail_1_9.sql |docker exec -i local-postgis psql -U postgres -d postgres