from peewee import *
from model import BaseModel, MyTimestampField
from model.user_model import UserModel
# 关注（对人） + 收藏（对文章）


class Follow(BaseModel):
    id = BlobField(primary_key=True)
    related_id = BlobField(index=True)  # 被关注对象
    related_type = IntegerField(index=True)  # 被关注对象的类型
    user_id = BlobField(index=True)  # 用户
    time = MyTimestampField(index=True)  # 发布时间

    class Meta:
        db_table = 'follow'
