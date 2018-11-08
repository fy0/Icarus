from peewee import *
from playhouse.postgres_ext import ArrayField, BinaryJSONField
from model import BaseModel, MyTimestampField
from model.board import Board
from model._post import POST_TYPES
from model.topic import Topic
from slim import json_ex_dumps


class PostStats(BaseModel):
    id = BlobField(primary_key=True)
    post_type = IntegerField(index=True)

    # all options
    last_comment_id = BlobField(null=True, default=None)
    viewed_users = ArrayField(BlobField, null=True)
    edited_users = ArrayField(BlobField, null=True)
    commented_users = ArrayField(BlobField, null=True)
    bookmarked_users = ArrayField(BlobField, null=True)
    upvoted_users = ArrayField(BlobField, null=True)
    downvoted_users = ArrayField(BlobField, null=True)
    thanked_users = ArrayField(BlobField, null=True)

    click_count = BigIntegerField(default=0)  # 点击数量，注意click和view并非一一对应的关系
    edit_count = BigIntegerField(default=0)  # 编辑次数
    comment_count = BigIntegerField(default=0)  # 评论数量
    topic_count = IntegerField(default=0)  # 主题数量
    follow_count = IntegerField(default=0)  # 关注数量
    bookmark_count = IntegerField(default=0)  # 收藏数量
    upvote_count = BigIntegerField(default=0)  # 赞同数量
    downvote_count = BigIntegerField(default=0)  # 反对数量
    thank_count = IntegerField(default=0)  # 感谢数量
    vote_weight = BigIntegerField(default=0, index=True)  # 权重

    # board
    # click_count = IntegerField(default=0)
    # comment_count = IntegerField(default=0)
    # topic_count = IntegerField(default=0)
    # last_comment_id = BlobField(null=True, default=None)

    # topic
    # viewed_users = ArrayField(BlobField, null=True)
    # commented_users = ArrayField(BlobField, null=True)
    # click_count = IntegerField(default=0)
    # comment_count = IntegerField(default=0)
    # follow_count = IntegerField(default=0)
    # last_comment_id = BlobField(null=True)

    # user
    # click_count = IntegerField(default=0)
    # comment_count = IntegerField(default=0)
    # follow_count = IntegerField(default=0)

    class Meta:
        db_table = 'post_stats'


class StatsLog(BaseModel):
    id = BlobField(primary_key=True)
    time = MyTimestampField(index=True)
    data = BinaryJSONField(dumps=json_ex_dumps)

    class Meta:
        db_table = 'stats_log'


def post_stats_add(field, user_id, post_type, post_id, related_id=None, num=1):
    pass


def post_stats_add_comment(related_type, related_id, comment_id):
    # 关于原子更新
    # http://docs.peewee-orm.com/en/latest/peewee/querying.html#atomic-updates
    # s: Statistic = cls.get_by_pk(related_id)
    PostStats.update(last_comment_id=comment_id, comment_count=PostStats.comment_count + 1)\
        .where(PostStats.id == related_id)\
        .execute()

    if related_type == POST_TYPES.TOPIC:
        t = Topic.get_by_pk(related_id)
        PostStats.update(last_comment_id=comment_id, comment_count=PostStats.comment_count + 1)\
            .where(PostStats.id == t.board_id)\
            .execute()


def post_stats_add_click(post_id):
    PostStats.update(click_count=PostStats.click_count + 1)\
        .where(PostStats.id == post_id)\
        .execute()


def post_stats_add_click_of_topic(topic_id, board_id=None):
    PostStats.update(click_count=PostStats.click_count + 1)\
        .where(PostStats.id == topic_id)\
        .execute()

    if not board_id:
        t = Topic.get_by_pk(topic_id)
        board_id = t.board_id

    PostStats.update(click_count=PostStats.click_count + 1)\
        .where(PostStats.id == board_id)\
        .execute()


def post_stats_board_add_topic(board_id, topic_id):
    PostStats.update(topic_count=PostStats.topic_count + 1)\
        .where(PostStats.id == board_id)\
        .execute()


def post_stats_topic_move(from_board_id, to_board_id, topic_id):
    # 修改评论数据
    ts = PostStats.get(PostStats.id == topic_id)
    if from_board_id:
        PostStats.update(topic_count=PostStats.topic_count - 1, comment_count=PostStats.comment_count - ts.comment_count)\
            .where(PostStats.id == from_board_id)\
            .execute()
    PostStats.update(topic_count=PostStats.topic_count + 1, comment_count=PostStats.comment_count + ts.comment_count)\
        .where(PostStats.id == to_board_id)\
        .execute()


def post_stats_new(post_type, id):
    PostStats.create(id=id, post_type=post_type)
