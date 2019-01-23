# Commercial Geographic Information Data: Unicom Big Data Population Insights

## Develop Environment
#### add config

```bash
cd <project root>
cp config/dev.tpl.py env.py 
```
_change the content of env.py_

#### run app
```bash
FLASK_APP=application FLASK_ENV=development flask run
```

## API
```bash
http://localhost:5000/api/populationInsights?lng=116.885482&lat=39.716071116&week=20180903
http://localhost:5000/api/populationInsights?lng=117.526198&lat=40.663529&week=20180903
```

## Data
```bash
export FLASK_APP=wrapper.py

flask db init
flask db migrate
flask db upgrade

#change to sql
./script/csv2sql.py grid -i ./data/csv -o ./data/sql V0110000
./script/csv2sql.py detail -i ./data/csv -o ./data/sql V0110000 20181029 20181105 20181112 20181119 20181126

#compress sql
./script/compress_sql grid -i ./data/sql -o ./data/tar V0110000
./script/compress_sql detail -i ./data/sql -o ./data/tar V0110000 20181029 20181105 20181112 20181119 20181126

#insert
./script/insert_sql grid -i ./data/tar -d local-postgis V0110000
./script/insert_sql detail -i ./data/tar -d local-postgis V0110000  20181029 20181105 20181112 20181119 20181126
./script/insert_sql all -i ./data/tar/t20190123 -d local-postgis-v2

# update
./script/csv2sql.py detail-update -d local-postgis -s ./data/tar/update/update1.sql.gz

# sync-csv
./script/csv2sql.py sync-csv -i xxx -o ./data
```


## Database
### Docker

#### Create docker network
``` shell
docker network create --subnet=172.18.0.0/16 local-lc
docker network ls
docker network inspect local-ls
```
#### Start postgresql server
``` shell
docker run -v /home/admin/pgdata-test:/var/lib/postgresql/data --restart=unless-stopped --name pg-cgid --network local-lc --ip 172.18.0.10 -e POSTGRES_PASSWORD=123456 -d mdillon/postgis:10
```
#### Start postgresql client
``` shell
docker run -it --rm --network local-lc mdillon/postgis:10 psql -h 172.18.0.10 -U postgres
```
#### pgadmin4 ??????????????????

``` shell
docker pull dpage/pgadmin4:3.6
docker run -p 80:80 -e "PGADMIN_DEFAULT_EMAIL=user@domain.com" -e "PGADMIN_DEFAULT_PASSWORD=123456" -d dpage/pgadmin4:3.6
```


## Other
+ WGS84 SRID:4326

## Question
+ map_grid表center字段是否必须?
+ week字段是每周第一天?怎么定位到这个字符串?
+ grid_id字段中'-1'需要特别注意么?