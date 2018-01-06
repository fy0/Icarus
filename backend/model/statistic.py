from peewee import *
from playhouse.postgres_ext import ArrayField, BinaryJSONField
from model import BaseModel, MyTimestampField
from model.user import User


class Statistic(BaseModel):
    id = BlobField(primary_key=True)

    # board
    click_count = IntegerField(default=0)
    comment_count = IntegerField(default=0)
    topic_count = IntegerField(default=0)

    # topic
    views = ArrayField(BlobField, null=True)
    # click_count = IntegerField(default=0)
    # comment_count = IntegerField(default=0)
    follow_count = IntegerField(default=0)

    # user
    # click_count = IntegerField(default=0)
    # comment_count = IntegerField(default=0)
    # follow_count = IntegerField(default=0)

    class Meta:
        db_table = 'statistic'


class Statistic24h(BaseModel):
    id = BlobField(primary_key=True)

    # board
    click_count = IntegerField(default=0)  # 24小时点击数
    comment_count = IntegerField(default=0)  # 24小时评论数
    topic_count = IntegerField(default=0)  # 24小时文章数

    # topic
    # click_count = IntegerField(default=0)
    # comment_count = IntegerField(default=0)
    follow_count = IntegerField(default=0)

    # user
    # click_count = IntegerField(default=0)
    # comment_count = IntegerField(default=0)
    # follow_count = IntegerField(default=0)

    class Meta:
        db_table = 'statistic24h'


class Statistic24hLog(BaseModel):
    id = BlobField(primary_key=True)
    time = MyTimestampField(index=True)
    data = BinaryJSONField()

    class Meta:
        db_table = 'statistic24h_log'


def statistic_new(id):
    Statistic.create(id=id)
    Statistic24h.create(id=id)
