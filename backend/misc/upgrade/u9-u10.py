import time
import peewee
from model import db
from model.user import User
from model.notif import UserNotifRecord


def work():
    try:
        db.execute_sql('ALTER TABLE "user" ADD COLUMN "visible" BYTEA NULL DEFAULT NULL;')
        db.execute_sql('ALTER TABLE "user" ADD COLUMN "user_id" BYTEA NULL DEFAULT NULL;')
        db.execute_sql('ALTER TABLE "user" RENAME "reg_time" TO "time";')
        db.execute_sql('ALTER TABLE "board" RENAME "creator_id" TO "user_id";')
        db.execute_sql('ALTER TABLE "comment" ADD COLUMN "post_number" INTEGER NULL;')

    except:
        print('failed')
        db.rollback()


if __name__ == '__main__':
    work()
    print('done')
