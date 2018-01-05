from slim.utils import StateObject
from peewee import *
from model import db, BaseModel, MyTimestampField
from model.user import User
from model.board import Board


class TOPIC_STATE(StateObject):
    DEL = 0
    HIDE = 10
    CLOSE = 30 # 禁止回复
    NORMAL = 50

    txt = {DEL: "删除", HIDE: "隐藏", CLOSE:"关闭", NORMAL:"正常"}


class Topic(BaseModel):
    id = BlobField(primary_key=True)
    title = TextField(index=True)
    user_id = BlobField(index=True)
    board_id = BlobField(index=True)
    time = MyTimestampField(index=True)
    state = IntegerField(default=TOPIC_STATE.NORMAL, index=True)

    edit_time = MyTimestampField(index=True, null=True)
    last_edit_user_id = BlobField(index=True, null=True)
    content = TextField()

    sticky_weight = IntegerField(index=True, default=0)  # 置顶权重
    weight = IntegerField(index=True, default=0) # 排序权值，越大越靠前，默认权重与id相同

    # object_type = OBJECT_TYPES.TOPIC

    class Meta:
        db_table = 'topic'

