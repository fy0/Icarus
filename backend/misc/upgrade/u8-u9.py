import time
import peewee
from model import db
from model.user_model import UserModel
from model.notif import UserNotifRecord


def work():
    try:
        db.execute_sql('ALTER TABLE "board" ADD COLUMN "parent_id" BYTEA NULL DEFAULT NULL;')
    except:
        print('failed')
        db.rollback()


if __name__ == '__main__':
    work()
    print('done')
