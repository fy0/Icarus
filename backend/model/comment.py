# coding:utf-8

import time
import config
from peewee import *
from model import BaseModel, MyTimestampField
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
    user_id = BlobField(index=True)  # 发布用户
    reply_to_cmt_id = BlobField(null=True)  # 是否指定回复某个评论
    time = MyTimestampField(index=True)  # 发布时间
    state = IntegerField(default=COMMENT_STATE.NORMAL)  # 当前状态
    content = TextField()  # 文本

    class Meta:
        db_table = 'comment'
