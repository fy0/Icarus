from peewee import BlobField, IntegerField, TextField
from playhouse.postgres_ext import BinaryJSONField
from slim import json_ex_dumps
from model._post import LongIdPostModel


class Mention(LongIdPostModel):
    who = BlobField(index=True)  # 被@的用户

    loc_post_type = IntegerField()  # 地点，类型
    loc_post_id = BlobField()  # 地点
    loc_post_title = TextField(null=True)  # 地点标题

    related_type = IntegerField(index=True)  # @相关对象的类型
    related_id = BlobField(index=True)  # @相关对象

    data = BinaryJSONField(dumps=json_ex_dumps, null=True)  # 附加数据，一般不需要了

    class Meta:
        db_table = 'mention'
