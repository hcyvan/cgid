import os
import sys
import csv
import argparse
import json
import math

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
    with open(file_path) as f:
        for row in csv.DictReader(f):
            key = '{}_{}'.format(row['city'], row['grid_id'])
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

    header = 'INSERT INTO detail (city, grid_id, week, stay, human_traffic, insight, consumption, mobile_phone) VALUES'
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
                    if stay or insight or human_traffic or consumption or mobile_phone:
                        stay = stay if stay else '{}'
                        insight = insight if insight else '{}'
                        human_traffic = human_traffic if human_traffic else '{}'
                        consumption = consumption if consumption else '{}'
                        mobile_phone = mobile_phone if mobile_phone else '[]'
                        sql = "('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}'),\n".format(
                            row['city'],
                            row['grid_id'],
                            week,
                            stay,
                            insight,
                            human_traffic,
                            consumption,
                            mobile_phone,
                            internet)
                        fo.write(sql.encode())
                fo.seek(-(len(os.linesep) + 1), os.SEEK_END)
                fo.write(';\n'.encode())


def grid(arg):
    trans_grid(arg.city, arg.input_dir, arg.output_dir)


def detail(arg):
    create_detail(arg.city, arg.week, arg.cut, arg.input_dir, arg.output_dir)


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
    parser_2 = subparsers.add_parser('detail', help='create xxx_insight.sql', parents=[parent_parser])
    parser_2.add_argument('city', action='store', help='city code')
    parser_2.add_argument('week', action='store', help='week string')
    parser_2.add_argument('-c', dest='cut', action='store', help='cut line number', type=int, default=100000)
    parser_2.set_defaults(func=detail)

    if len(sys.argv) == 1:
        args_list = ['-h']
    else:
        args_list = sys.argv[1:]

    args = parser.parse_args(args_list)
    args.func(args)
