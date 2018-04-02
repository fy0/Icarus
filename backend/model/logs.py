from peewee import *
from playhouse.postgres_ext import BinaryJSONField
from model import BaseModel, MyTimestampField
from model.user import User
from slim import json_ex_dumps


class ManageLog(BaseModel):
    id = BlobField(primary_key=True)
    user_id = BlobField(index=True)  # 操作用户
    time = MyTimestampField(index=True)  # 操作时间
    related_id = BlobField(index=True)  # 被操作对象
    related_type = IntegerField()  # 被操作对象类型
    operation = IntegerField()  # 操作行为
    value = BinaryJSONField(dumps=json_ex_dumps)  # 操作数据

    class Meta:
        db_table = 'manage_log'
