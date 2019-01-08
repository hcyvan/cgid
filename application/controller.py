import time

from flask import Blueprint, request, jsonify, current_app
from sqlalchemy import func

from .model import Grid, Detail, User, Access
from config import const
from .helper import timestamp2week_label, timestamp2day_label, get_token

api = Blueprint('api', __name__)


@api.route('/populationInsights')
def get_data():
    cid = request.args.get('cid')
    timestamp = request.args.get('timestamp')
    token = request.args.get('token')

    if None in [cid, timestamp, token]:
        return jsonify(dict(
            code=1001,
            msg='auth info is needed'
        ))
    user = User.query.get(cid)
    if not user:
        return jsonify(dict(
            code=1002,
            msg='user not exist'
        ))
    token_local = get_token(user.id, user.password, timestamp)
    if token_local != token:
        return jsonify(dict(
            code=1003,
            msg='wrong token'
        ))
    if time.time() - int(timestamp) > current_app.config['EXPIRE_TIME']:
        return jsonify(dict(
            code=1004,
            msg='token expired'
        ))

    day = timestamp2day_label(time.time())
    access = Access.query.filter_by(cid=cid, day=day).first()
    if access is None:
        access = Access(cid=cid, day=day, count=1)
        access.save()
    else:
        if access.count > 5000:
            return jsonify(dict(
                code=1021,
                msg='visits overflow'
            ))
        access.count = access.count + 1
        access.update()

    lng = request.args.get('lng')
    lat = request.args.get('lat')
    ts = request.args.get('ts')
    week = timestamp2week_label(ts)

    grid = Grid.query.filter(func.ST_Contains(
        Grid.box, 'SRID={};POINT({} {})'.format(const.get('SRID'), lng, lat))).first()

    if not grid:
        ret = dict(
            code=1031,
            msg='不具备访问该坐标的权限'
        )
    else:
        detail = Detail.query.filter_by(city=grid.city, grid_id=grid.grid_id, week=week).first()
        if not detail:
            ret = dict(
                code=1032,
                msg='不具备访问该时间的权限'
            )
        else:
            ret = dict(
                code=0,
                data=dict(
                    stay=detail.stay,
                    mobile_phone=detail.mobile_phone,
                    consumption=detail.consumption,
                    human_traffic=detail.human_traffic,
                    insight=detail.insight,
                    internet=detail.internet
                )
            )

    return jsonify(ret)
