from flask import Blueprint, request, jsonify
from sqlalchemy import func

from .model import Grid
from config import const

api = Blueprint('api', __name__)


@api.route('/populationInsights')
def get_data():
    lng = request.args.get('lng')
    lat = request.args.get('lat')
    grid = Grid.query.filter(func.ST_Contains(
        Grid.box, 'SRID={};POINT({} {})'.format(const.get('SRID'), lng, lat))).first()

    if grid:
        if grid.stay:
            grid.stay.pop('week')
        if grid.mobile_phone:
            for i, _ in enumerate(grid.mobile_phone):
                grid.mobile_phone[i].pop('week')
        if grid.consumption:
            grid.consumption.pop('week')
        if grid.human_traffic:
            grid.human_traffic.pop('week')
        if grid.insight:
            grid.insight.pop('week')
        ret = dict(
            code=0,
            data=dict(
                stay=grid.stay,
                mobile_phone=grid.mobile_phone,
                consumption=grid.consumption,
                human_tranffic=grid.human_traffic,
                insight=grid.insight
            )
        )
    else:
        ret = dict(
            code=1001,
            msg='不具备访问该坐标的权限'
        )
    return jsonify(ret)
