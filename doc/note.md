+ 删除旧文件: find ./* ! -newermt '2019-10-30' -type f|xargs rm
+ xargs的批处理: find ./ |grep grid|xargs -i mv {} ../grid/



## psql
+ select pg_size_pretty(pg_database_size()): 查看数据库的大小
+ select pg_size_pretty(pg_relation_size()): 查看数据表的大小,不包含索引
+ select pg_size_pretty(pg_total_relation_size()): 查看数据表的大小,包含索引等
