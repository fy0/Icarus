import time
import peewee
from model import db
from model.comment_model import CommentModel
from model.user_model import UserModel
from model.notif import UserNotifRecord


def work():
    try:
        db.execute_sql('DROP TABLE statistic24h;')
        db.execute_sql('ALTER TABLE "user" ADD COLUMN "visible" INTEGER NULL DEFAULT NULL;')
        db.execute_sql('ALTER TABLE "user" ADD COLUMN "user_id" BYTEA NULL DEFAULT NULL;')
        db.execute_sql('ALTER TABLE "user" ADD COLUMN "reset_key" BYTEA NULL DEFAULT NULL;')
        db.execute_sql('ALTER TABLE "user" ADD COLUMN "avatar" TEXT NULL DEFAULT NULL;')
        db.execute_sql('ALTER TABLE "user" ADD COLUMN "type" INTEGER DEFAULT 0;')
        db.execute_sql('ALTER TABLE "user" ADD COLUMN "url" TEXT NULL DEFAULT NULL;')
        db.execute_sql('ALTER TABLE "user" ADD COLUMN "location" TEXT NULL DEFAULT NULL;')
        db.execute_sql('ALTER TABLE "user" ADD COLUMN "access_time" BIGINT NULL DEFAULT NULL;')
        db.execute_sql('ALTER TABLE "user" ADD COLUMN "last_check_in_time" BIGINT NULL DEFAULT NULL;')
        db.execute_sql('ALTER TABLE "user" ADD COLUMN "check_in_his" INT DEFAULT 0;')
        db.execute_sql('ALTER TABLE "user" ADD COLUMN "exp" INT DEFAULT 0;')

        db.execute_sql('ALTER TABLE "user" RENAME "reg_time" TO "time";')
        db.execute_sql('ALTER TABLE "board" RENAME "creator_id" TO "user_id";')
        db.execute_sql('ALTER TABLE "comment" ADD COLUMN "post_number" INTEGER NULL;')

        db.execute_sql('ALTER TABLE "statistic" ADD COLUMN "bookmark_count" INTEGER DEFAULT 0;')
        db.execute_sql('ALTER TABLE "statistic" ADD COLUMN "upvote_count" INTEGER DEFAULT 0;')
        db.execute_sql('ALTER TABLE "statistic" ADD COLUMN "downvote_count" INTEGER DEFAULT 0;')
        db.execute_sql('ALTER TABLE "statistic" ADD COLUMN "thank_count" INTEGER DEFAULT 0;')
        db.execute_sql('ALTER TABLE "statistic" ADD COLUMN "vote_weight" BIGINT DEFAULT 0;')
        db.execute_sql('ALTER TABLE "statistic" ADD COLUMN "bookmarked_users" BYTEA[] NULL;')
        db.execute_sql('ALTER TABLE "statistic" ADD COLUMN "upvoted_users" BYTEA[] NULL;')
        db.execute_sql('ALTER TABLE "statistic" ADD COLUMN "downvoted_users" BYTEA[] NULL;')
        db.execute_sql('ALTER TABLE "statistic" ADD COLUMN "thanked_users" BYTEA[] NULL;')
    except Exception as e:
        print(e)
        print('failed')
        db.rollback()

    for i in CommentModel.select():
        post_number = CommentModel.select().where(CommentModel.related_id == i.related_id, CommentModel.id <= i.id).count()
        CommentModel.update(post_number=post_number).where(CommentModel.id == i.id).execute()


if __name__ == '__main__':
    work()
    print('done')
