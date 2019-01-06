import time
import hashlib

from flask import Blueprint, request, jsonify
from sqlalchemy import func

from .model import Grid, Detail, User, Access
from config import const
from .helper import timestamp2week_label, timestamp2day_label

api = Blueprint('api', __name__)


def check_token(cid, timestamp, token):
    if None in [cid, timestamp, token]:
        return False
    user = User.query.get(cid)
    if not user:
        return False
    h = hashlib.sha256()
    h.update((user.id + user.password + timestamp).encode())
    if h.hexdigest() != token:
        return False
    if time.time() - int(timestamp) > 5 * 600:
        return False
    return True


@api.route('/populationInsights')
def get_data():
    cid = request.args.get('cid')
    timestamp = request.args.get('timestamp')
    token = request.args.get('token')

    if not check_token(cid, timestamp, token):
        return jsonify(dict(
            code=1001,
            msg='您无访问权限'
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
                msg='超出访问次数'
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
            code=1001,
            msg='不具备访问该坐标的权限'
        )
    else:
        detail = Detail.query.filter_by(city=grid.city, grid_id=grid.grid_id, week=week).first()
        if not detail:
            ret = dict(
                code=1002,
                msg='不具备访问该时间的权限'
            )
        else:
            ret = dict(
                code=0,
                data=dict(
                    stay=detail.stay,
                    mobile_phone=detail.mobile_phone,
                    consumption=detail.consumption,
                    human_tranffic=detail.human_traffic,
                    insight=detail.insight
                )
            )

    return jsonify(ret)
