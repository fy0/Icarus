import datetime
import time
from peewee import *
from slim.utils.state_obj import StateObject

from model import BaseModel
from model.user import User


def today_midnight():
    today = datetime.date.today()
    return time.mktime(today.timetuple())


class BOARD_STATE(StateObject):
    DEL = 0
    BAN = 20
    HIDE = 30
    NORMAL = 50

    txt = {DEL: '删除', BAN: '禁止', HIDE: '隐藏', NORMAL: '正常'}


class Board(BaseModel):
    id = BlobField(primary_key=True)
    title = TextField(unique=True)  # max 128
    creator = ForeignKeyField(User, null=True)
    brief = TextField(null=True)  # max 256
    desc = TextField(null=True)  # max 1024
    time = BigIntegerField(index=True)
    weight = IntegerField(index=True, default=0)
    color = BlobField(null=True, default=None)
    state = IntegerField(default=BOARD_STATE.NORMAL)
    # + category

    default_colors = ['#fda34b', '#59b3d0', '#a26bc2', '#FF5555', '#86C1B9', '#AB4642', '#777777', '#42b983',
                      '#3d5dff', '#e0cb45', '#BA8BAF', '#7CAFC2']

    class Meta:
        db_table = 'board'
