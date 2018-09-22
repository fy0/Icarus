import datetime
import time
from peewee import *
from model._post import POST_VISIBLE, POST_STATE, PostModel
from slim.utils.state_obj import StateObject
from model import BaseModel, MyTimestampField
from model.user import User


def today_midnight():
    today = datetime.date.today()
    return time.mktime(today.timetuple())


class Board(PostModel):
    name = TextField(unique=True)  # max 128
    parent_id = BlobField(index=True, null=True, default=None)  # 上级板块ID
    brief = TextField(null=True)  # max 256
    desc = TextField(null=True)  # max 1024
    weight = IntegerField(index=True, default=0)
    color = BlobField(null=True, default=None)
    category = TextField(null=True)  # 大分类，默认为空

    default_colors = ['#fda34b', '#59b3d0', '#a26bc2', '#FF5555', '#86C1B9', '#AB4642', '#777777', '#42b983',
                      '#3d5dff', '#e0cb45', '#BA8BAF', '#7CAFC2']

    class Meta:
        db_table = 'board'

    def get_title(self):
        return self.name
