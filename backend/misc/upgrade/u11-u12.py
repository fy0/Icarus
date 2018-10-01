"""
如果执行失败，请将此文件复制到backend目录再次执行。
"""
import time
import peewee
from model import db
from model._post import POST_STATE
from model.comment import Comment
from model.user import User, USER_GROUP
from model.notif import UserNotifLastInfo


def sql_execute(sql):
    try:
        db.execute_sql(sql)
    except Exception as e:
        print(e)
        print('failed')
        db.rollback()


def work():
    sql_execute('ALTER TABLE "user" ALTER COLUMN number TYPE SERIAL;')
    sql_execute('''ALTER TABLE "user" ALTER COLUMN number SET DEFAULT nextval('user_count_seq');''')


if __name__ == '__main__':
    work()
    print('done')
