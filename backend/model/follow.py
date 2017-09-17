from peewee import *
from model import BaseModel
from model.user import User


class Follow(BaseModel):
    id = BlobField(primary_key=True)
    related_id = BlobField(index=True)  # 被关注对象
    related_type = IntegerField(index=True)  # 被关注对象的类型
    user = ForeignKeyField(User)  # 用户
    time = BigIntegerField(index=True)  # 发布时间

    class Meta:
        db_table = 'follow'
