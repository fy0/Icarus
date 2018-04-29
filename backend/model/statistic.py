from peewee import *
from playhouse.postgres_ext import ArrayField, BinaryJSONField
from model import BaseModel, MyTimestampField
from model.board import Board
from model.post import POST_TYPES
from model.topic import Topic
from slim import json_ex_dumps


class Statistic(BaseModel):
    id = BlobField(primary_key=True)
    post_type = IntegerField(index=True)

    # board
    click_count = IntegerField(default=0)
    comment_count = IntegerField(default=0)
    topic_count = IntegerField(default=0)
    last_comment_id = BlobField(null=True, default=None)

    # topic
    viewed_users = ArrayField(BlobField, null=True)
    commented_users = ArrayField(BlobField, null=True)
    # click_count = IntegerField(default=0)
    # comment_count = IntegerField(default=0)
    follow_count = IntegerField(default=0)
    # last_comment_id = BlobField(null=True)

    # user
    # click_count = IntegerField(default=0)
    # comment_count = IntegerField(default=0)
    # follow_count = IntegerField(default=0)

    class Meta:
        db_table = 'statistic'


class Statistic24h(BaseModel):
    id = BlobField(primary_key=True)
    post_type = IntegerField(index=True)

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
    data = BinaryJSONField(dumps=json_ex_dumps)

    class Meta:
        db_table = 'statistic24h_log'


def statistic_add_comment(related_type, related_id, comment_id):
    # 关于原子更新
    # http://docs.peewee-orm.com/en/latest/peewee/querying.html#atomic-updates
    # s: Statistic = cls.get_by_pk(related_id)
    Statistic.update(last_comment_id=comment_id, comment_count=Statistic.comment_count + 1)\
        .where(Statistic.id == related_id)\
        .execute()
    Statistic24h.update(comment_count=Statistic24h.comment_count + 1)\
        .where(Statistic24h.id == related_id)\
        .execute()

    if related_type == POST_TYPES.TOPIC:
        t = Topic.get_by_pk(related_id)
        Statistic.update(last_comment_id=comment_id, comment_count=Statistic.comment_count + 1)\
            .where(Statistic.id == t.board_id)\
            .execute()
        Statistic24h.update(comment_count=Statistic24h.comment_count + 1)\
            .where(Statistic24h.id == t.board_id)\
            .execute()


def statistic_add_topic_click(topic_id, board_id=None):
    Statistic.update(click_count=Statistic.click_count + 1)\
        .where(Statistic.id == topic_id)\
        .execute()

    Statistic24h.update(click_count=Statistic24h.click_count + 1)\
        .where(Statistic24h.id == topic_id)\
        .execute()

    if not board_id:
        t = Topic.get_by_pk(topic_id)
        board_id = t.board_id

    Statistic.update(click_count=Statistic.click_count + 1)\
        .where(Statistic.id == board_id)\
        .execute()

    Statistic24h.update(click_count=Statistic24h.click_count + 1)\
        .where(Statistic24h.id == board_id)\
        .execute()


def statistic_add_topic(board_id, topic_id):
    Statistic.update(topic_count=Statistic.topic_count + 1)\
        .where(Statistic.id == board_id)\
        .execute()
    Statistic24h.update(topic_count=Statistic24h.topic_count + 1)\
        .where(Statistic24h.id == board_id)\
        .execute()


def statistic_move_topic(from_board_id, to_board_id, topic_id):
    if from_board_id:
        Statistic.update(topic_count=Statistic.topic_count - 1)\
            .where(Statistic.id == from_board_id)\
            .execute()
        Statistic24h.update(topic_count=Statistic24h.topic_count - 1)\
            .where(Statistic24h.id == from_board_id)\
            .execute()
    Statistic.update(topic_count=Statistic.topic_count + 1)\
        .where(Statistic.id == to_board_id)\
        .execute()
    Statistic24h.update(topic_count=Statistic24h.topic_count + 1)\
        .where(Statistic24h.id == to_board_id)\
        .execute()


def statistic_new(post_type, id):
    Statistic.create(id=id, post_type=post_type)
    Statistic24h.create(id=id, post_type=post_type)
