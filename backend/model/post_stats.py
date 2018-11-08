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


def post_stats_incr(field: Field, post_id, num=1, callback=None):
    update_data = {field.name: field + num}
    where = [PostStats.id == post_id]
    if callback: callback(update_data, where)

    PostStats.update(**update_data)\
        .where(*where) \
        .execute()


def post_stats_do_comment(related_type, related_id, comment_id):
    # 关于原子更新
    # http://docs.peewee-orm.com/en/latest/peewee/querying.html#atomic-updates

    # 更新自身数据
    def func(update_data, where): update_data['last_comment_id'] = comment_id
    post_stats_incr(PostStats.comment_count, related_id, 1, callback=func)

    if related_type == POST_TYPES.TOPIC:
        # 更新板块数据
        t = Topic.get_by_pk(related_id)
        post_stats_incr(PostStats.comment_count, t.board_id, 1, callback=func)


def post_stats_add_topic_click(topic_id, board_id=None):
    if not board_id:
        t = Topic.get_by_pk(topic_id)
        board_id = t.board_id
    post_stats_incr(PostStats.click_count, topic_id)
    post_stats_incr(PostStats.click_count, board_id)


def post_stats_topic_move(from_board_id, to_board_id, topic_id):
    # 修改评论数据
    ts = PostStats.get(PostStats.id == topic_id)
    if from_board_id:
        def func(update_data, where):
            update_data['comment_count'] = PostStats.comment_count - ts.comment_count
        post_stats_incr(PostStats.topic_count, from_board_id, -1, callback=func)

    def func(update_data, where):
        update_data['comment_count'] = PostStats.comment_count + ts.comment_count
    post_stats_incr(PostStats.topic_count, to_board_id, 1, callback=func)


def post_stats_new(post_type, id):
    PostStats.create(id=id, post_type=post_type)


def post_stats_topic_new(board_id, topic_id):
    post_stats_incr(PostStats.topic_count, board_id)
    post_stats_new(POST_TYPES.TOPIC, topic_id)
