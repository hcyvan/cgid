from flask import Blueprint, request, jsonify
from sqlalchemy import func

from .model import Grid, Detail
from config import const
from .helper import timestamp2label

api = Blueprint('api', __name__)


@api.route('/populationInsights')
def get_data():
    lng = request.args.get('lng')
    lat = request.args.get('lat')
    ts = request.args.get('ts')
    week = timestamp2label(ts)

    grid = Grid.query.filter(func.ST_Contains(
        Grid.box, 'SRID={};POINT({} {})'.format(const.get('SRID'), lng, lat))).first()

    if not grid:
        ret = dict(
            code=1001,
            msg='不具备访问该坐标的权限'
        )
    else:
        detail = Detail.query.filter_by(city=grid.city, grid_id=grid.grid_id, week=week).first()
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
