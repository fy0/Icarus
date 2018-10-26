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
        print('failed: %s' % sql)
        db.rollback()


def work():
    sql_execute('drop table "wiki_history";')
    sql_execute('drop table "wiki_item";')
    sql_execute('drop table "wiki_article";')


if __name__ == '__main__':
    work()
    print('done')
