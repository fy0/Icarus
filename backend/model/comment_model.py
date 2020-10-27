# coding:utf-8

from peewee import *
from model import BaseModel, MyTimestampField
from model._post import POST_STATE, POST_VISIBLE, LongIdPostModel, POST_TYPES


class CommentModel(LongIdPostModel):
    related_id = BlobField(index=True)  # 被评论文章
    related_type = IntegerField(index=True)  # 被评论文章的类型
    reply_to_cmt_id = BlobField(null=True)  # 是否指定回复某个评论
    content = TextField()  # 文本
    post_number = IntegerField(null=True)  # 楼层数

    class Meta:
        db_table = 'comment'

    @classmethod
    def get_post_type(cls):
        return POST_TYPES.COMMENT
