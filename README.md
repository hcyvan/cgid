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
/api/populationInsights?lng=116&lat=39.9&week=20180903
```

## Data
```bash
export FLASK_APP=wrapper.py

flask db init
flask db migrate
flask db upgrade

flask csv2sql
flask insert-sql ./data/map_grid.sql
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
docker run --restart=unless-stopped --name local-postgis --network local-lc --ip 172.18.0.10 -e POSTGRES_PASSWORD=123456 -d mdillon/postgis:10
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