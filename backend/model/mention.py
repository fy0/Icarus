from peewee import BlobField, IntegerField, TextField
from playhouse.postgres_ext import BinaryJSONField
from slim import json_ex_dumps
from model._post import LongIdPostModel


class Mention(LongIdPostModel):
    who = BlobField(index=True)  # 被@的用户
    related_id = BlobField(index=True)  # @相关对象
    related_type = IntegerField(index=True)  # @相关对象的类型
    data = BinaryJSONField(dumps=json_ex_dumps, null=True)  # 附加数据

    class Meta:
        db_table = 'mention'
