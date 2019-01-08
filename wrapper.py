import time
import os
import click
from flask_migrate import Migrate
from flask.cli import with_appcontext

from application import create_app
from application.ext import db
from application.model import User
from application.helper import get_token

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
    exec_sql_file('./script/truncate_table.sql')


@app.cli.command('add-user')
@with_appcontext
@click.argument('cid')
@click.argument('password')
def add_user(cid, password):
    user = User.query.filter_by(id=cid).first()
    if user:
        print('Cid: {} exist!'.format(cid))
    else:
        user = User(id=cid, password=password)
        user.save()
        print('Create User Successfully')


@app.cli.command('create-url')
@click.argument('cid')
@click.argument('password')
def gen(cid, password):
    time.time()
    lng = 116.885482
    lat = 39.716071116
    ts = 1540828800
    timestamp = int(time.time())
    token = get_token(cid, password, timestamp)
    url = 'http://localhost:5000/api/populationInsights?lng={}&lat={}&ts={}&cid={}&timestamp={}&token={}'.format(lng,
                                                                                                                 lat,
                                                                                                                 ts,
                                                                                                                 cid,
                                                                                                                 timestamp,
                                                                                                                 token)
    print(url)
