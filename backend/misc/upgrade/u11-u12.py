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
        print('failed: %s' % sql)
        db.rollback()


def work():
    sql_execute('''ALTER TABLE "user" ALTER COLUMN number SET DEFAULT nextval('user_count_seq');''')
    sql_execute('ALTER TABLE "user" ADD phone_verified boolean DEFAULT FALSE NULL;')
    sql_execute('ALTER TABLE "user" ADD change_nickname_chance int DEFAULT 0 NULL;')

    sql_execute('ALTER TABLE "user" ALTER COLUMN email DROP NOT NULL;')
    sql_execute('ALTER TABLE "user" ALTER COLUMN email SET DEFAULT NULL;')

    sql_execute('ALTER TABLE "user" ALTER COLUMN phone DROP NOT NULL;')
    sql_execute('ALTER TABLE "user" ALTER COLUMN phone SET DEFAULT null;')
    sql_execute('CREATE UNIQUE INDEX user_phone ON "user" (phone);')
    sql_execute('ALTER TABLE "user" ALTER COLUMN nickname DROP NOT NULL;')

    sql_execute('ALTER TABLE "user" RENAME COLUMN reputation TO repute;')
    sql_execute('ALTER TABLE "user" ADD is_new_user BOOLEAN DEFAULT TRUE  NOT NULL;')

    # 注册的激活机制改了，变通一下吧
    for i in UserModel.select().where(UserModel.group == USER_GROUP.INACTIVE):
        i.group = USER_GROUP.NORMAL
        i.save()

    # 老用户全部设置为非新用户
    for i in UserModel.select().where(UserModel.is_new_user == False):
        i.is_new_user = True
        i.save()


if __name__ == '__main__':
    work()
    print('done')
