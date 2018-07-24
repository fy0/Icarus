from peewee import BlobField, IntegerField, TextField
from model._post import LongIdPostModel


class Mention(LongIdPostModel):
    who = BlobField(index=True)  # 被@的用户
    related_id = BlobField(index=True)  # @相关对象
    related_type = IntegerField(index=True)  # @相关对象的类型

    class Meta:
        db_table = 'mention'
