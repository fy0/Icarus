import time

from model._post import POST_VISIBLE, POST_STATE, PostModel, POST_TYPES
from model.redis import RK_TOPIC_WEIGHT_MAX, redis
from slim.utils import StateObject
from peewee import *
from model import db, BaseModel, MyTimestampField
from model.user_model import UserModel
from model.board_model import BoardModel

"""
顶贴机制：
1. 置顶权重，默认为0，如有置顶则设置其值，越高排在越上面
2. 一般权重，默认值为发帖时当前帖子个数，回帖、上升、下沉几个操作使其增加或减少，越高排在越上面
3. 时间，当以上两个权重相等的时候，越新的帖子排在越上面
"""


class TopicModel(PostModel):
    title = TextField(index=True)
    board_id = BlobField(index=True)

    edit_count = IntegerField(default=0)
    edit_time = MyTimestampField(index=True, null=True)
    last_edit_user_id = BlobField(index=True, null=True)
    content = TextField()

    awesome = IntegerField(default=0)  # 精华文章
    sticky_weight = IntegerField(index=True, default=0)  # 置顶权重
    weight = IntegerField(index=True, default=0)  # 排序权值，越大越靠前，默认权重与id相同
    update_time = BigIntegerField(index=True, null=True, default=None)  # 更新时间，即发布的时间或最后被回复的时间
    # comment_time = BigIntegerField(index=True, null=True, default=None)  # 更新时间，即发布的时间或最后被回复的时间

    # object_type = OBJECT_TYPES.TOPIC

    class Meta:
        db_table = 'topic'

    @classmethod
    async def weight_redis_init(cls):
        cur = db.execute_sql('select max(weight)+1 from "topic"')
        await redis.set(RK_TOPIC_WEIGHT_MAX, cur.fetchone()[0] or 0)

    @classmethod
    async def weight_gen(cls):
        """ 提升一点权重上限"""
        return int(await redis.incr(RK_TOPIC_WEIGHT_MAX))

    async def weight_inc(self):
        """ 提升一点排序权重，但不能高于最大权重 """
        self.weight = min(self.weight + 1, int(await redis.get(RK_TOPIC_WEIGHT_MAX)))
        self.update_time = int(time.time())
        self.save()

    '''
    async def comment_update(self):
        self.comment_time = int(time.time())
        self.save()
    '''

    @classmethod
    def get_post_type(cls):
        return POST_TYPES.TOPIC

    def get_title(self):
        return self.title
