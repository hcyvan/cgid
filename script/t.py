#!/usr/bin/env python3
import glob
import os


city_sql_path = './data/sql/V0530100/'

city = 'V0530100'
week = '20181126'

p = os.path.join(city_sql_path, '{}_{}_detail*sql'.format(city, week))

for sql in glob.glob(p):
    print(sql)