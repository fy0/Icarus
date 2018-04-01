# coding:utf-8

from peewee import *
from model import BaseModel, MyTimestampField
from model.post import POST_STATE, POST_VISIBLE


class Comment(BaseModel):
    id = BlobField(primary_key=True)
    related_id = BlobField(index=True)  # 被评论文章
    related_type = IntegerField(index=True)  # 被评论文章的类型
    user_id = BlobField(index=True)  # 发布用户
    reply_to_cmt_id = BlobField(null=True)  # 是否指定回复某个评论
    time = MyTimestampField(index=True)  # 发布时间
    state = IntegerField(default=POST_STATE.NORMAL)  # 当前状态
    visible = IntegerField(default=POST_VISIBLE.NORMAL, index=True)
    content = TextField()  # 文本

    class Meta:
        db_table = 'comment'
