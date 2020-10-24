import time
import peewee
from model import db
from model import _models
from model.user_model import UserModel
from model.notif import UserNotifRecord


def work():
    try:
        db.execute_sql('ALTER TABLE public.comment ADD reply_to_cmt_id BYTEA NULL;')
    except:
        db.rollback()

    for i in UserModel.select().execute():
        try:
            UserNotifRecord.create(id=i.id, update_time=int(time.time()))
        except peewee.IntegrityError:
            db.rollback()


if __name__ == '__main__':
    work()
    print('done')
