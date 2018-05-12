import time
from peewee import *
from playhouse.postgres_ext import ArrayField, BinaryJSONField
import config
from model import BaseModel, MyTimestampField, db
from model._post import POST_STATE
from model.user import User
from slim import json_ex_dumps
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
          "t"."title", left("c".content, 50), "u"."nickname"
        FROM topic AS t, comment AS c, "user" as u
        WHERE t.user_id = %s AND t.state >= %s AND t.id = c.related_id
          AND c.id > %s AND c.state >= %s AND u.id = c.user_id AND "c"."user_id" != "t"."user_id"
        ORDER BY "c"."id" DESC
        ''', (user_id, POST_STATE.CLOSE, last_comment_id, POST_STATE.NORMAL))
    # 时间，评论ID，文章ID，POST类型，用户ID，文章标题，前50个字，用户昵称

    def wrap(i):
        return {
            'type': NOTIF_TYPE.BE_COMMENTED,
            'time': i[0],
            'post': {
                'id': i[2],
                'type': i[3],
                'title': i[5]
            },
            'comment': {
                'id': i[1],
                'brief': i[6],
                'user': {
                    'id': i[4],
                    'nickname': i[7]
                }
            }
        }
    return map(wrap, cur.fetchall())


def fetch_notif_of_reply(user_id, last_reply_id=b'\x00'):
    # 某某 在文章 某某某 中回复了你的评论： XXXXXX
    # c2 是 user_id 的原评论，c 是回复评论的评论
    cur = db.execute_sql('''
        SELECT "c".time, "c"."id", "c"."related_id", "c"."related_type", "c".user_id, 
          "t"."title", left("c".content, 50), "u"."nickname"
        FROM topic AS t, comment AS c, comment AS c2, "user" as u
        WHERE c2.user_id = %s AND c2.state >= %s AND
          c2.id = c.reply_to_cmt_id AND c.id > %s AND c.state >= %s AND t.id = c.related_id
          AND u.id = c.user_id AND "c"."user_id" != "c2"."user_id" -- 不查自己
        ORDER BY "c"."id" DESC
        ''', (user_id, POST_STATE.NORMAL, last_reply_id, POST_STATE.NORMAL))
    # 时间，评论ID，文章ID，POST类型，用户ID，文章标题，前50个字，用户昵称

    def wrap(i):
        return {
            'type': NOTIF_TYPE.BE_REPLIED,
            'time': i[0],
            'post': {
                'id': i[2],
                'type': i[3],
                'title': i[5]
            },
            'comment': {
                'id': i[1],
                'brief': i[6],
                'user': {
                    'id': i[4],
                    'nickname': i[7]
                }
            }
        }
    return map(wrap, cur.fetchall())


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
    update_time = MyTimestampField(index=True)

    @classmethod
    def new(cls, user_id):
        try:
            return cls.create(id=user_id, update_time=int(time.time()))
        except IntegrityError:
            db.rollback()

    def get_notifications(self, update_last=False):
        lst = []
        l1 = tuple(fetch_notif_of_comment(self.id, self.last_comment_id))
        l2 = tuple(fetch_notif_of_reply(self.id, self.last_reply_id))
        lst.extend(l1)
        lst.extend(l2)
        # lst.sort(key = lambda x: x['time'], reverse=True)

        if update_last:
            if l1: self.last_comment_id = l1[0]['comment']['id']
            if l2: self.last_reply_id = l2[0]['comment']['id']
            self.update_time = int(time.time())
            self.save()

        return lst

    class Meta:
        db_table = 'user_notif_record'


class Notification(BaseModel):
    id = BlobField(primary_key=True)
    sender_ids = ArrayField(BlobField)
    receiver_id = BlobField(index=True)
    type = IntegerField(index=True)
    time = MyTimestampField(index=True)  # 发布时间
    data = BinaryJSONField(dumps=json_ex_dumps)
    is_read = BooleanField(default=False)

    @classmethod
    def count(cls, user_id):
        return cls.select().where(cls.receiver_id == user_id, cls.is_read == False).count()

    @classmethod
    def set_read(cls, user_id):
        cur = db.execute_sql('''
        WITH updated_rows as (
          UPDATE notif SET is_read = TRUE WHERE "receiver_id" = %s AND "is_read" = FALSE
          RETURNING is_read
        ) SELECT count(is_read) FROM updated_rows;
        ''', (user_id,))
        return cur.fetchone()[0]

    @classmethod
    def refresh(cls, user_id, cooldown = config.NOTIF_FETCH_COOLDOWN):
        new = []
        r: UserNotifRecord = UserNotifRecord.get_by_pk(user_id)
        if not r: return
        if cooldown and (time.time() - r.update_time < cooldown):
            return
        for i in r.get_notifications(True):
            if i['type'] == NOTIF_TYPE.BE_COMMENTED:
                new.append({
                    'id': config.LONG_ID_GENERATOR().to_bin(),
                    'sender_ids': (i['comment']['user']['id'],),
                    'receiver_id': user_id,
                    'type': NOTIF_TYPE.BE_COMMENTED,
                    'time': i['time'],
                    'data': i,
                })
            elif i['type'] == NOTIF_TYPE.BE_REPLIED:
                new.append({
                    'id': config.LONG_ID_GENERATOR().to_bin(),
                    'sender_ids': (i['comment']['user']['id'],),
                    'receiver_id': user_id,
                    'type': NOTIF_TYPE.BE_REPLIED,
                    'time': i['time'],
                    'data': i,
                })

        if new:
            cls.insert_many(new).execute()
        return len(new)

    class Meta:
        db_table = 'notif'


if __name__ == '__main__':
    u: User = User.select().where(User.nickname == '折影').get()
    r: UserNotifRecord = UserNotifRecord.get_by_pk(u.id)
    for i in r.get_notifications():
        print(i)
    print('------')
    # Notification.refresh(u.id)
