# coding:utf-8

import time
import config
from peewee import *
from model import BaseModel
from model.user import User
from model.board import Board
from slim.utils import StateObject


class COMMENT_STATE(StateObject):
    DEL = 0
    HIDE = 10
    NORMAL = 50


class Comment(BaseModel):
    id = BlobField(primary_key=True)
    related_id = BlobField(index=True)  # 被评论文章
    related_type = IntegerField(index=True)  # 被评论文章的类型
    extra_id = BlobField(index=True, null=True)  # 关联ID
    user = ForeignKeyField(User)  # 发布用户
    send_to_id = BlobField(null=True)  # 是否是回复某个评论
    time = BigIntegerField(index=True)  # 发布时间
    state = IntegerField(default=COMMENT_STATE.NORMAL)  # 当前状态
    content = TextField()  # 文本，varchar(4096)

    class Meta:
        db_table = 'comment'
