"""
提醒系统

这个文件在决定引入 redis 之前写就，所以目前为止是只与SQL数据库相关的
Notification 这个类直接对应用户的提醒界面数据，用户与 Notification 对象是一对多的
UserNotifLastInfo 记录了多个用户最后的时间点，与用户是一对一的

提醒记录不主动写入，只当有必要的时候（例如用户上线后）才进行获取，以节省资源。
而方式就是通过 UserNotifLastInfo 中的数据去查询对应的表，并生成 Notification 记录
"""

import time
from peewee import *
from playhouse.postgres_ext import ArrayField, BinaryJSONField
import config
from model import BaseModel, MyTimestampField, db
from model._post import POST_STATE, POST_TYPES
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
    # TODO: 仅支持文章的抓取
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

            'loc_post_type': i[3],
            'loc_post_id': i[2],
            'loc_post_title': i[5],

            'sender_ids': (i[4],),
            'receiver_id': user_id,

            'related_type': POST_TYPES.COMMENT,
            'related_id': i[1],

            'brief': i[6],
        }
    return map(wrap, cur.fetchall())


def fetch_notif_of_reply(user_id, last_reply_id=b'\x00'):
    # TODO: 还是仅支持文章
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

            'loc_post_type': i[3],
            'loc_post_id': i[2],
            'loc_post_title': i[5],

            'sender_ids': (i[4],),
            'receiver_id': user_id,

            'related_type': POST_TYPES.COMMENT,
            'related_id': i[1],

            'brief': i[6]
        }
    return map(wrap, cur.fetchall())


def fetch_notif_of_metion(user_id, last_mention_id=b'\x00'):
    # 某某 在文章 某某某 中@了你： XXXXXX
    # c2 是 user_id 的原评论，c 是回复评论的评论
    from .mention import Mention
    item_lst = Mention.select().where(Mention.who == user_id, Mention.id > last_mention_id).order_by(Mention.id.desc())
    # lst = [[m.related_type, m.related_id] for m in item_lst]
    # title_map = POST_TYPES.get_post_title_by_list(*lst)

    def wrap(mt: Mention):
        return {
            'type': NOTIF_TYPE.BE_MENTIONED,
            'time': mt.time,

            'loc_post_type': mt.loc_post_type,
            'loc_post_id': mt.loc_post_id,
            'loc_post_title': mt.loc_post_title,

            'sender_ids': (mt.user_id,),
            'receiver_id': user_id,

            'related_type': POST_TYPES.MENTION,
            'related_id': mt.id,
        }
    return map(wrap, item_lst)


class UserNotifLastInfo(BaseModel):
    id = BlobField(primary_key=True)  # user_id
    last_be_commented_id = BlobField(default=b'\x00')
    last_be_replied_id = BlobField(default=b'\x00')
    last_be_followed_id = BlobField(default=b'\x00')
    last_be_mentioned_id = BlobField(default=b'\x00')
    last_be_bookmarked_id = BlobField(default=b'\x00')
    last_be_liked_id = BlobField(default=b'\x00')
    last_be_sent_pm_id = BlobField(default=b'\x00')
    last_received_sysmsg_id = BlobField(default=b'\x00')
    update_time = MyTimestampField(index=True)

    @classmethod
    def new(cls, user_id):
        try:
            return cls.create(id=user_id, update_time=int(time.time()))
        except IntegrityError:
            db.rollback()

    def get_notifications(self, update_last=False):
        lst = []
        l1 = tuple(fetch_notif_of_comment(self.id, self.last_be_commented_id))
        l2 = tuple(fetch_notif_of_reply(self.id, self.last_be_replied_id))
        l3 = tuple(fetch_notif_of_metion(self.id, self.last_be_mentioned_id))
        lst.extend(l1)
        lst.extend(l2)
        lst.extend(l3)

        if update_last:
            if l1: self.last_be_commented_id = l1[0]['related_id']
            if l2: self.last_be_replied_id = l2[0]['related_id']
            if l3: self.last_be_mentioned_id = l3[0]['related_id']
            self.update_time = int(time.time())
            self.save()

        return lst

    class Meta:
        db_table = 'user_notif_last_info'


class Notification(BaseModel):
    id = BlobField(primary_key=True)
    type = IntegerField(index=True)  # 行为
    time = MyTimestampField(index=True)  # 行为发生时间

    loc_post_type = IntegerField()  # 地点，类型
    loc_post_id = BlobField()  # 地点
    loc_post_title = TextField(null=True)  # 地点标题

    sender_ids = ArrayField(BlobField)  # 人物，行为方
    receiver_id = BlobField(index=True)  # 人物，被动方

    related_type = IntegerField(null=True)  # 可选，关联类型
    related_id = BlobField(null=True)  # 可选，关联ID。例如A在B帖回复C，人物是A和C，地点是B，关联是这个回复的ID

    brief = TextField(null=True)  # 一小段预览，可有可无

    data = BinaryJSONField(dumps=json_ex_dumps, null=True)  # 附加数据
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
        r: UserNotifLastInfo = UserNotifLastInfo.get_by_pk(user_id)
        if not r: return
        if cooldown and (time.time() - r.update_time < cooldown):
            return

        def pack_notif(i):
            i.update({
                'id': config.LONG_ID_GENERATOR().to_bin()
            })
            return i

        newlst = r.get_notifications(True)
        newlst.sort(key = lambda x: x['time'], reverse=True)
        newlst = list(map(pack_notif, newlst))

        if newlst:
            cls.insert_many(newlst).execute()
        return len(newlst)

    class Meta:
        db_table = 'notif2'


if __name__ == '__main__':
    u: User = User.select().where(User.nickname == '折影').get()
    r: UserNotifLastInfo = UserNotifLastInfo.get_by_pk(u.id)
    for i in r.get_notifications():
        print(i)
    print('------')
    # Notification.refresh(u.id)
