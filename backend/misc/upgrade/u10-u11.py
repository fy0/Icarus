import time
import peewee
from model import db
from model.comment import Comment
from model.user import User
from model.notif import UserNotifRecord


def work():
    try:
        db.execute_sql('ALTER TABLE "topic" ADD COLUMN "update_time" BIGINT NULL DEFAULT NULL ;')
    except Exception as e:
        print(e)
        print('failed')
        db.rollback()


if __name__ == '__main__':
    work()
    print('done')
