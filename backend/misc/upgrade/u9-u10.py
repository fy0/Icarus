import time
import peewee
from model import db
from model.comment import Comment
from model.user import User
from model.notif import UserNotifRecord


def work():
    try:
        db.execute_sql('ALTER TABLE "user" ADD COLUMN "visible" INTEGER NULL DEFAULT NULL;')
        db.execute_sql('ALTER TABLE "user" ADD COLUMN "user_id" BYTEA NULL DEFAULT NULL;')
        db.execute_sql('ALTER TABLE "user" RENAME "reg_time" TO "time";')
        db.execute_sql('ALTER TABLE "board" RENAME "creator_id" TO "user_id";')
        db.execute_sql('ALTER TABLE "comment" ADD COLUMN "post_number" INTEGER NULL;')

    except:
        print('failed')
        db.rollback()

    for i in Comment.select():
        post_number = Comment.select().where(Comment.related_id == i.related_id, Comment.id <= i.id).count()
        Comment.update(post_number=post_number).where(Comment.id == i.id).execute()


if __name__ == '__main__':
    work()
    print('done')
