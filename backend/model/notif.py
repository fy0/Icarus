from peewee import *
from model import BaseModel, MyTimestampField
from model.user import User
from slim.utils import StateObject


class NOTIF_TYPE(StateObject):
    BE_COMMENTED = 10  # 被评论/回复
    BE_FOLLOWED  = 20  # 被关注
    BE_MENTIONED = 30  # 被提及(@)
    BE_BOOKMARKED = 40 # 被收藏
    BE_LIKED      = 50 # 被赞
    BE_SENT_PM    = 60 # 被发私信
    SYSTEM_MSG    = 100


class Notification(BaseModel):
    id = BlobField(primary_key=True)
    sender_id = BlobField()
    receiver_id = BlobField(index=True)
    type = IntegerField(index=True)
    time = MyTimestampField(index=True)  # 发布时间

    # senders 发送者
    # times 次数
    # read 已读

    class Meta:
        db_table = 'notif'
