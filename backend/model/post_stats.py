import time
from peewee import *
from playhouse.postgres_ext import ArrayField, BinaryJSONField
from model import BaseModel, MyTimestampField
from model.board_model import BoardModel
from model._post import POST_TYPES
from model.topic_model import TopicModel
from slim import json_ex_dumps


class PostStatsModel(BaseModel):
    id = BlobField(primary_key=True)
    post_type = IntegerField(index=True)

    last_comment_id = BlobField(null=True, default=None)
    last_edit_user_id = BlobField(null=True, default=None)
    last_edit_time = BigIntegerField(null=True, default=None)
    update_time = BigIntegerField(null=True, default=None, index=True)

    click_count = BigIntegerField(default=0)  # 点击数量
    edit_count = IntegerField(default=0)  # 编辑次数
    comment_count = IntegerField(default=0)  # 评论数量
    topic_count = IntegerField(default=0)  # 主题数量
    follow_count = IntegerField(default=0)  # 关注数量
    bookmark_count = IntegerField(default=0)  # 收藏数量
    upvote_count = IntegerField(default=0)  # 赞同数量
    downvote_count = IntegerField(default=0)  # 反对数量
    thank_count = IntegerField(default=0)  # 感谢数量
    vote_weight = IntegerField(default=0, index=True)  # 权重

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


def post_stats_incr(field: Field, post_id, num=1, cb=None):
    # 关于原子更新
    # http://docs.peewee-orm.com/en/latest/peewee/querying.html#atomic-updates
    update_data = {field.name: field + num}
    where = [PostStatsModel.id == post_id]
    if cb: cb(update_data, where)

    PostStatsModel.update(**update_data)\
        .where(*where) \
        .execute()


def post_stats_do_edit(post_id, user_id):
    def func(update, where):
        update['last_edit_user_id'] = user_id
        update['last_edit_time'] = int(time.time())
        update['update_time'] = int(time.time())
    post_stats_incr(PostStatsModel.edit_count, post_id, cb=func)


def post_stats_do_comment(related_type, related_id, comment_id):
    # 需要同时更新被评论对象的数字和最后评论id
    def func(update, where): update['last_comment_id'] = comment_id
    post_stats_incr(PostStatsModel.comment_count, related_id, 1, cb=func)

    # 如果被评论的是文章，需要更新板块数据
    if related_type == POST_TYPES.TOPIC:
        t = TopicModel.get_by_pk(related_id)
        post_stats_incr(PostStatsModel.comment_count, t.board_id, 1, cb=func)


def post_stats_add_topic_click(topic_id, board_id=None):
    if not board_id:
        t = TopicModel.get_by_pk(topic_id)
        board_id = t.board_id
    post_stats_incr(PostStatsModel.click_count, topic_id)
    post_stats_incr(PostStatsModel.click_count, board_id)


def post_stats_topic_move(from_board_id, to_board_id, topic_id):
    # 修改评论数据
    ts = PostStatsModel.get(PostStatsModel.id == topic_id)
    if from_board_id:
        def func(update_data, where):
            update_data['comment_count'] = PostStatsModel.comment_count - ts.comment_count
        post_stats_incr(PostStatsModel.topic_count, from_board_id, -1, cb=func)

    def func(update_data, where):
        update_data['comment_count'] = PostStatsModel.comment_count + ts.comment_count
    post_stats_incr(PostStatsModel.topic_count, to_board_id, 1, cb=func)


def post_stats_new(post_type, id):
    PostStatsModel.create(id=id, post_type=post_type, update_time=int(time.time()))


def post_stats_topic_new(board_id, topic_id):
    post_stats_incr(PostStatsModel.topic_count, board_id)
    post_stats_new(POST_TYPES.TOPIC, topic_id)
