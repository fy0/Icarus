from peewee import *
from model import BaseModel, MyTimestampField
from model.user import User
from slim.utils import StateObject


class NOTIF_TYPE(StateObject):
    BE_COMMENTED = 10  # 被评论
    BE_FOLLOWED  = 20  # 被关注
    BE_MENTIONED = 30  # 被提及(@)


class Notification(BaseModel):
    id = BlobField(primary_key=True)
    type = IntegerField(index=True)
    time = MyTimestampField(index=True)  # 发布时间

    class Meta:
        db_table = 'notif'
