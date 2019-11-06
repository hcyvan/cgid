+ 删除旧文件: find ./* ! -newermt '2019-10-30' -type f|xargs rm
+ xargs的批处理: find ./ |grep grid|xargs -i mv {} ../grid/