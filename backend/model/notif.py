from peewee import *
from playhouse.postgres_ext import ArrayField, BinaryJSONField

from model import BaseModel, MyTimestampField, db
from model.comment import COMMENT_STATE
from model.topic import TOPIC_STATE
from model.user import User
from slim.utils import StateObject


class NOTIF_TYPE(StateObject):
    BE_COMMENTED  = 10  # 被评论
    BE_REPLIED    = 20  # 被回复
    BE_FOLLOWED   = 30  # 被关注
    BE_MENTIONED  = 40  # 被提及(@)
    BE_BOOKMARKED = 50 # 被收藏
    BE_LIKED      = 60 # 被赞
    BE_SENT_PM    = 70 # 被发私信
    SYSTEM_MSG    = 100


# 注意：目前仅支持文章的评论提醒，未来的其他类型以后另算


def fetch_notif_of_comment(user_id, last_comment_id=b'\x00'):
    # 某某 评论了你的文章 某某某： XXXXXX
    # 这个暂时不折叠了，全部显示在提醒中
    cur = db.execute_sql('''
        SELECT "c".time, "c"."id", "c"."related_id", "c"."related_type", "c".user_id, 
          "t"."title", left("c".content, 50)
        FROM topic as t, comment as c
        WHERE t.user_id = %s and t.state >= %s and
          t.id = c.related_id and c.id > %s and c.state >= %s
        ''', (user_id, TOPIC_STATE.CLOSE, last_comment_id, COMMENT_STATE.NORMAL))
    # 时间，评论ID，文章ID，POST类型，用户ID，文章标题，前50个字
    return cur.fetchall()


def fetch_notif_of_reply(user_id, last_reply_id=b'\x00'):
    # 某某 在文章 某某某 中回复了你的评论： XXXXXX
    # c2 是 user_id 的原评论，c 是回复评论的评论
    cur = db.execute_sql('''
        SELECT "c".time, "c"."id", "c"."related_id", "c"."related_type", "c".user_id, 
          "t"."title", left("c".content, 50)
        FROM topic AS t, comment AS c, comment AS c2
        WHERE c2.user_id = %s AND c2.state >= %s AND
          c2.id = c.reply_to_cmt_id AND c.id > %s AND c.state >= %s AND t.id == c.related_id
        ''', (user_id, COMMENT_STATE.NORMAL, last_reply_id, COMMENT_STATE.NORMAL))
    # 时间，评论ID，文章ID，POST类型，用户ID，文章标题，前50个字
    return cur.fetchall()


class UserNotifRecord(BaseModel):
    id = BlobField(primary_key=True)  # user_id
    last_comment_id = BlobField(default=b'\x00')
    last_reply_id = BlobField(default=b'\x00')
    last_follow_id = BlobField(default=b'\x00')
    last_mention_id = BlobField(default=b'\x00')
    last_bookmark_id = BlobField(default=b'\x00')
    last_like_id = BlobField(default=b'\x00')
    last_pm_id = BlobField(default=b'\x00')
    last_sysmsg_id = BlobField(default=b'\x00')
    update_time = MyTimestampField()

    def get_notifications(self):
        lst = []
        l1 = fetch_notif_of_comment(self.id, self.last_comment_id)
        l2 = fetch_notif_of_reply(self.id, self.last_reply_id)
        lst.extend(l1)
        lst.extend(l2)
        lst.sort(key = lambda x: x[0])
        return lst

    class Meta:
        db_table = 'user_notif_record'


class Notification(BaseModel):
    id = BlobField(primary_key=True)
    sender_ids = ArrayField(BlobField)
    receiver_id = BlobField(index=True)
    type = IntegerField(index=True)
    time = MyTimestampField(index=True)  # 发布时间
    data = BinaryJSONField()
    is_read = BooleanField(default=False)

    class Meta:
        db_table = 'notif'
