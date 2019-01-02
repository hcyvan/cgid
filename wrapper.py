import os
import click
from flask_migrate import Migrate

from application import create_app
from application.ext import db
from application.model import *
from csv2sql import create_value

app = create_app()

Migrate(app, db)


def get_sql(sql_file):
    sql_file_path = os.path.join(app.root_path, '..', sql_file)
    with open(sql_file_path) as f:
        sql = f.read()
    return sql


def exec_sql_file(sql_file):
    db.engine.execute(get_sql(sql_file))


@app.cli.command()
def clear_data():
    exec_sql_file('./sql/truncate_table.sql')


@app.cli.command()
@click.argument('sql_path')
def insert_sql(sql_path):
    exec_sql_file(sql_path)


@app.cli.command()
def csv2sql():
    import csv
    input_file = os.path.join(app.root_path, '../data', 'map_grid.csv')
    output_file = os.path.join(app.root_path, '../data', 'map_grid.sql')

    config = {
        'table': 'grid',
        'sql_key': ['city', 'grid_id', 'center', 'box'],
        'sql_key_type': ['string', 'string', 'geometry:point', 'geometry:polygon'],
        'csv_key': ['city', 'grid_id', 'center', 'box'],
    }
    header = 'INSERT INTO {} ({}) VALUES'.format(config['table'], ', '.join(config['sql_key']))
    i = 0
    with open(input_file) as fi:
        for _ in csv.DictReader(fi):
            i = i + 1
    with open(input_file) as fi, open(output_file, 'w') as fo:
        fo.write(header + '\n')
        input_csv = csv.DictReader(fi)
        for j, row in enumerate(input_csv):
            values = [row.get(x) for x in config['sql_key']]
            value_sql = create_value(values, config['sql_key_type'])
            if i == j + 1:
                fo.write(value_sql + ';\n')
            else:
                fo.write(value_sql + ',\n')
