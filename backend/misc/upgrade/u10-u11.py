"""
如果执行失败，请将此文件复制到backend目录再次执行。
"""
import time
import peewee
from model import db
from model._post import POST_STATE
from model.comment_model import CommentModel
from model.user_model import UserModel, USER_GROUP
from model.notif import UserNotifLastInfo


def sql_execute(sql):
    try:
        db.execute_sql(sql)
    except Exception as e:
        print(e)
        print('failed')
        db.rollback()


def work():
    sql_execute('ALTER TABLE "topic" ADD COLUMN "update_time" BIGINT NULL DEFAULT NULL ;')
    sql_execute('ALTER TABLE "user" ADD COLUMN "ip_registered" inet NULL DEFAULT NULL;')
    sql_execute('drop table "notif";')
    sql_execute('drop table "mention";')
    sql_execute('drop table "user_notif_record";')

    db.create_tables([UserNotifLastInfo], safe=True)
    for i in UserModel.select().execute():
        try:
            UserNotifLastInfo.create(id=i.id, update_time=int(time.time()))
        except peewee.IntegrityError as e:
            print(e)
            db.rollback()

    # 之前的 INACTIVE
    # 放弃了这个设定，INACTIVE作为USER_GROUP也没有太大问题
    # User.update(state=POST_STATE.INACTIVE, group=USER_GROUP.NORMAL).where(User.group == 40)


if __name__ == '__main__':
    work()
    print('done')
