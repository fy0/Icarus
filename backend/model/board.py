import datetime
import time
from peewee import *

from model.post import POST_VISIBLE, POST_STATE
from slim.utils.state_obj import StateObject

from model import BaseModel, MyTimestampField
from model.user import User


def today_midnight():
    today = datetime.date.today()
    return time.mktime(today.timetuple())


class Board(BaseModel):
    id = BlobField(primary_key=True, constraints=[SQL("DEFAULT int2bytea(nextval('id_gen_seq'))")])
    name = TextField(unique=True)  # max 128
    creator_id = BlobField(index=True, null=True)  # 创建者ID
    brief = TextField(null=True)  # max 256
    desc = TextField(null=True)  # max 1024
    time = MyTimestampField(index=True)  # 创建时间
    weight = IntegerField(index=True, default=0)
    color = BlobField(null=True, default=None)
    state = IntegerField(default=POST_STATE.NORMAL)
    visible = IntegerField(default=POST_VISIBLE.NORMAL, index=True)
    category = TextField(null=True)  # 大分类，默认为空

    default_colors = ['#fda34b', '#59b3d0', '#a26bc2', '#FF5555', '#86C1B9', '#AB4642', '#777777', '#42b983',
                      '#3d5dff', '#e0cb45', '#BA8BAF', '#7CAFC2']

    class Meta:
        db_table = 'board'
