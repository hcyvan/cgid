import os
import csv
import json
import math

SRID = '4326'
DATA_PATH = './data'


def create_value(values, ftypes):
    if len(values) != len(ftypes):
        raise Exception('csv2sql config: values and ftypes have different length!')
    value_insert = []
    for i, value in enumerate(values):
        if ftypes[i] == 'string' or ftypes[i] == 'jsonb':
            value_format = "'{}'".format(value)
        elif ftypes[i] == 'geometry:point':
            value_format = "ST_GeomFromText('POINT({})', {})".format(
                value, SRID)
        elif ftypes[i] == 'geometry:polygon':
            value_format = "ST_GeomFromText('POLYGON{}', {})".format(
                value[1:-1], SRID)
        else:
            value_format = value
        value_insert.append(value_format)
    return '({})'.format(', '.join(value_insert))


def get_dict(file_path, value_type='dict'):
    print('Reading {}'.format(file_path))
    data = dict()
    with open(file_path) as f:
        for row in csv.DictReader(f):
            key = '{}_{}'.format(row['city'], row['grid_id'])
            row.pop('city', None)
            row.pop('grid_id', None)
            if value_type == 'list':
                if data.get(key, None) is None:
                    data[key] = [row]
                else:
                    data[key].append(row)
            else:
                data[key] = row
    return data


city = 'V0110000'
week = '20180903'
cut = 30000

output_file = os.path.join(DATA_PATH, '{}_{}_grid.sql'.format(city, week))
table_names = ('grid', 'stay', 'mobilePhone', 'consumption', 'humanTraffic', 'insight')
files = [os.path.join(DATA_PATH, '{}_{}_{}.csv'.format(city, week, x)) for x in table_names]

stay_map = get_dict(files[1])
mobile_phone_map = get_dict(files[2], value_type='list')
consumption_map = get_dict(files[3])
human_traffic_map = get_dict(files[4])
insight_map = get_dict(files[5])

input_file = files[0]

config = {
    'table': 'grid',
    'sql_key': ['city',
                'grid_id',
                'box',
                'stay',
                'mobile_phone',
                'consumption',
                'human_traffic',
                'insight'],
    'sql_key_type': ['string',
                     'string',
                     'geometry:polygon',
                     'jsonb',
                     'jsonb',
                     'jsonb',
                     'jsonb',
                     'jsonb'],
    'csv_key': ['city',
                'grid_id',
                'box',
                'jsonb:stay',
                'jsonb:mobile_phone',
                'jsonb:consumption',
                'jsonb:human_traffic',
                'jsonb:insight'],
}

header = 'INSERT INTO {} ({}) VALUES'.format(config['table'], ', '.join(config['sql_key']))
with open(input_file) as fi:
    rows = [x for x in csv.DictReader(fi)]
    row_num = len(rows)
    sql_num = math.ceil(row_num / cut)
    print('Total row: {}, split to {} files, each row have {} line'.format(row_num, sql_num, cut))
    for i in range(sql_num):
        names = output_file.split('.')
        output_sql_file = '{}_{}_{}.{}'.format('.'.join(names[:-1]), i + 1, sql_num, names[-1])
        start = i * cut
        end = (i + 1) * cut if (i + 1) * cut <= row_num else row_num
        print('Writing to {}: from line {} to line {}.'.format(output_sql_file, start+1, end))

        with open(output_sql_file, 'w') as f:
            f.write(header + '\n')
            for j, row in enumerate(rows[start:end]):
                values = []
                for x in config['csv_key']:
                    key = '{}_{}'.format(row['city'], row['grid_id'])
                    if x == 'jsonb:stay':
                        data = json.dumps(stay_map.get(key))
                    elif x == 'jsonb:mobile_phone':
                        data = json.dumps(mobile_phone_map.get(key))
                    elif x == 'jsonb:consumption':
                        data = json.dumps(consumption_map.get(key))
                    elif x == 'jsonb:human_traffic':
                        data = json.dumps(human_traffic_map.get(key))
                    elif x == 'jsonb:insight':
                        data = json.dumps(insight_map.get(key))
                    else:
                        data = row.get(x)
                    values.append(data)
                value_sql = create_value(values, config['sql_key_type'])
                if start + j + 1 == end:
                    f.write(value_sql + ';\n')
                else:
                    f.write(value_sql + ',\n')
