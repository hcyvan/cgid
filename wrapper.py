import os
import click
from flask_migrate import Migrate

from application import create_app
from application.ext import db
from application.model import *

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

