#!/usr/bin/env python3

import os
import gzip
import tarfile
from datetime import datetime
import sys
import csv
import argparse
import json
import math
import shutil

SRID = '4326'


def get_row_num(file_name):
    """
    Count row line number, except file header.
    :param file_name:
    :return:
    """
    num = 0
    with open(file_name) as f:
        for _ in csv.DictReader(f):
            num = num + 1
    return num


def get_dict(file_path, value_type='object'):
    print('Reading {}'.format(file_path))
    data = dict()
    city = os.path.basename(file_path).split('_')[0]
    with open(file_path) as f:
        for row in csv.DictReader(f):
            key = '{}_{}'.format(city, row['grid_id'])
            row.pop('city', None)
            row.pop('grid_id', None)
            row.pop('week', None)
            if value_type == 'list':
                if data.get(key, None) is None:
                    data[key] = '<list>//{}'.format(json.dumps(row))
                else:
                    data[key] = data[key] + '//{}'.format(json.dumps(row))
            else:
                data[key] = json.dumps(row)
    return data


def trans_grid(city, input_dir='./', output_dir='./'):
    grid_file = os.path.join(input_dir, '{}_grid.csv'.format(city))
    sql_file = os.path.join(output_dir, '{}_grid.sql'.format(city))
    grid_num = get_row_num(grid_file)
    with open(grid_file) as fi, open(sql_file, 'w') as fo:
        fo.write('INSERT INTO grid (city, grid_id, box) VALUES\n')
        for i, row in enumerate(csv.DictReader(fi)):
            sql = "('{}', '{}', {})".format(
                row['city'],
                row['grid_id'],
                "ST_GeomFromText('POLYGON{}', {})".format(row['box'][1:-1], SRID))
            if i + 1 == grid_num:
                sql = sql + ';\n'
            else:
                sql = sql + ',\n'
            fo.write(sql)


def create_detail(city, week, cut, input_dir='./', output_dir='./'):
    grid_file = os.path.join(input_dir, '{}_grid.csv'.format(city))
    sql_file = os.path.join(output_dir, '{}_{}_detail.sql'.format(city, week))

    tables = ['stay', 'insight', 'humanTraffic', 'consumption', 'mobilePhone', 'internet']
    files = [os.path.join(input_dir, '{}_{}_{}.csv'.format(city, week, x)) for x in tables]

    def find_grid_detail(dictionary, city, grid_id):
        key = '{}_{}'.format(city, grid_id)
        _detail = dictionary.get(key, None)
        if _detail:
            if _detail.startswith('<list>'):
                return '[{}]'.format(','.join(_detail.split('//')[1:]))
            else:
                return _detail
        else:
            return None

    stay_dict = get_dict(files[0])
    insight_dict = get_dict(files[1])
    human_traffic_dict = get_dict(files[2])
    consumption_dict = get_dict(files[3])
    mobile_phone_dict = get_dict(files[4], value_type='list')
    internet_dict = get_dict(files[5], value_type='list')
    # stay_dict = {}
    # insight_dict = {}
    # human_traffic_dict = {}
    # consumption_dict = {}
    # mobile_phone_dict = {}
    # internet_dict = {}

    header = 'INSERT INTO detail (city, grid_id, week, stay, human_traffic, insight, consumption, mobile_phone, internet) VALUES'
    with open(grid_file) as fi:
        rows = [x for x in csv.DictReader(fi)]
        row_num = len(rows)
        sql_num = math.ceil(row_num / cut)
        print('Total row: {}, split to {} files, each row have {} line'.format(row_num, sql_num, cut))
        for i in range(sql_num):
            names = sql_file.split('.')
            output_sql_file = '{}_{}_{}.{}'.format('.'.join(names[:-1]), i + 1, sql_num, names[-1])
            start = i * cut
            end = (i + 1) * cut if (i + 1) * cut <= row_num else row_num
            print('Writing to {}: from line {} to line {}.'.format(output_sql_file, start + 1, end))

            with open(output_sql_file, 'wb') as fo:
                fo.write((header + '\n').encode())
                for j, row in enumerate(rows[start:end]):
                    city = row['city']
                    grid_id = row['grid_id']
                    stay = find_grid_detail(stay_dict, city, grid_id)
                    insight = find_grid_detail(insight_dict, city, grid_id)
                    human_traffic = find_grid_detail(human_traffic_dict, city, grid_id)
                    consumption = find_grid_detail(consumption_dict, city, grid_id)
                    mobile_phone = find_grid_detail(mobile_phone_dict, city, grid_id)
                    internet = find_grid_detail(internet_dict, city, grid_id)
                    stay = stay if stay else '{}'
                    insight = insight if insight else '{}'
                    human_traffic = human_traffic if human_traffic else '{}'
                    consumption = consumption if consumption else '{}'
                    mobile_phone = mobile_phone if mobile_phone else '[]'
                    internet = internet if internet else '[]'
                    sql = "('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}'),\n".format(
                        row['city'],
                        row['grid_id'],
                        week,
                        stay,
                        human_traffic,
                        insight,
                        consumption,
                        mobile_phone,
                        internet)
                    fo.write(sql.encode())
                fo.seek(-(len(os.linesep) + 1), os.SEEK_END)
                fo.write(';\n'.encode())


def grid(arg):
    trans_grid(arg.city, arg.input_dir, arg.output_dir)


def detail(arg):
    for week in arg.week:
        print('Handle week {} ...'.format(week))
        create_detail(arg.city, week, arg.cut, arg.input_dir, arg.output_dir)


def detail_update(arg):
    sql_path = os.path.join(arg.output_dir, arg.sql)
    for csv_file in os.listdir(arg.input_dir):
        csv_path = os.path.join(arg.input_dir, csv_file)
        print('Handling {} ...'.format(csv_file))
        city, week, item, = csv_file.split('.')[0].split('_')
        with open(csv_path) as fi, gzip.open(sql_path, 'wb') as fo:
            for line in csv.DictReader(fi):
                grid_id = line.pop('grid_id')
                stay = json.dumps(line)
                sql = "UPDATE detail SET {}='{}' WHERE city='{}' and grid_id='{}' and week='{}';\n".format(item,
                                                                                                           stay,
                                                                                                           city,
                                                                                                           grid_id,
                                                                                                           week)
                fo.write(sql.encode())


def sync_csv(arg):
    """
    Synchronize csv data
    file_map
        {
            <city_id>: {
                grid: xxxx;
                <week1>: [],
                <week2>: [],
                ...
            }
            ...
        }
    :param arg:
    :return:
    """
    files = os.listdir(arg.input_dir)
    file_map = dict()
    for f in files:
        label = os.path.splitext(f)[0].split('_')
        if file_map.get(label[0], None) is None:
            file_map[label[0]] = dict()
        if label[1] == 'grid':
            file_map[label[0]]['grid'] = f
        else:
            if file_map[label[0]].get('data', None) is None:
                file_map[label[0]]['data'] = dict()
            if file_map[label[0]]['data'].get(label[1], None) is None:
                file_map[label[0]]['data'][label[1]] = []
            file_map[label[0]]['data'][label[1]].append(f)
    tar_name = 't{}'.format(datetime.now().strftime('%Y%m%d'))
    tar_path = os.path.join(arg.output_dir, 'tar', tar_name)
    if not os.path.exists(tar_path):
        os.mkdir(tar_path)
    i = 0
    n = len(file_map)
    for city, v in file_map.items():
        i = i + 1
        print('------ handle city [{}/{}]: {} -------'.format(i, n, city))
        city_csv_path = os.path.join(arg.output_dir, 'csv', city)
        city_sql_path = os.path.join(arg.output_dir, 'sql', city)
        if not os.path.exists(city_csv_path):
            os.mkdir(city_csv_path)
        if not os.path.exists(city_sql_path):
            os.mkdir(city_sql_path)
        grid = v.get('grid', None)
        if grid:
            grid = os.path.splitext(grid)[0]
            print('** handling grid ...')
            shutil.copyfile(os.path.join(arg.input_dir, '{}.csv'.format(grid)),
                            os.path.join(city_csv_path, '{}.csv'.format(grid)))
            # trans_grid(k, city_csv_path, city_sql_path)
            print('****** GZIP grid sql')
            with open(os.path.join(city_sql_path, '{}.sql'.format(grid))) as fi, gzip.open(
                    os.path.join(tar_path, '{}.sql.gz'.format(grid)), 'wb') as fo:
                fo.write(fi.read().encode())
        data = v.get('data', None)
        if data:
            print('** handling data ...')
            for week, data_files in data.items():
                print('**** week: {}'.format(week))
                for data_file in data_files:
                    shutil.copyfile(os.path.join(arg.input_dir, data_file), os.path.join(city_csv_path, data_file))
                # create_detail(k, week, 30000, city_csv_path, city_sql_path)
                print('****** TAR detail sql')
                with tarfile.open(os.path.join(tar_path, '{}_{}_detail.sql.tar.gz'.format(city, week)), 'w:gz') as f:
                    for city_week_detail in os.listdir(city_sql_path):
                        if city_week_detail.startswith('{}_{}_detail'.format(city, week)):
                            f.add(os.path.join(city_sql_path, city_week_detail), arcname=city_week_detail)


if __name__ == '__main__':
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('-i', '--input-dir', default='./', action='store', help='input file dir')
    parent_parser.add_argument('-o', '--output-dir', default='./', action='store', help='output file dir')
    parser = argparse.ArgumentParser(description='Unicom Big Data Population Insights: CSV data to Sql')
    subparsers = parser.add_subparsers(help='Handle csv data')

    # grid
    parser_1 = subparsers.add_parser('grid', help='create xxx_grid.sql', parents=[parent_parser])
    parser_1.add_argument('city', action='store', help='city code')
    parser_1.set_defaults(func=grid)

    # detail
    parser_2 = subparsers.add_parser('detail', help='create xxx_detail.sql', parents=[parent_parser])
    parser_2.add_argument('-c', dest='cut', action='store', help='cut line number', type=int, default=30000)
    parser_2.add_argument('city', action='store', help='city code')
    parser_2.add_argument('week', nargs='*', action='store', help='week string')
    parser_2.set_defaults(func=detail)

    # detail-update
    parser_3 = subparsers.add_parser('detail-update', help='create update sql', parents=[parent_parser])
    parser_3.add_argument('-c', dest='cut', action='store', help='cut line number', type=int, default=0)
    parser_3.add_argument('-s', dest='sql', action='store', help='update sql file', default='update.sql')
    parser_3.set_defaults(func=detail_update)

    # sync-csv
    parser_4 = subparsers.add_parser('sync-csv', help='Synchronize csv data', parents=[parent_parser])
    parser_4.set_defaults(func=sync_csv)

    if len(sys.argv) == 1:
        args_list = ['-h']
    else:
        args_list = sys.argv[1:]

    args = parser.parse_args(args_list)
    args.func(args)
