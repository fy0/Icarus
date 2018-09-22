import time
import peewee
from model import db
from model._post import POST_STATE
from model.comment import Comment
from model.user import User, USER_GROUP
from model.notif import UserNotifLastInfo


def work():
    try:
        db.execute_sql('ALTER TABLE "topic" ADD COLUMN "update_time" BIGINT NULL DEFAULT NULL ;')
    except Exception as e:
        print(e)
        print('failed')
        db.rollback()

    # 之前的 INACTIVE
    # 放弃了这个设定，INACTIVE作为USER_GROUP没有问题
    # User.update(state=POST_STATE.INACTIVE, group=USER_GROUP.NORMAL).where(User.group == 40)


if __name__ == '__main__':
    work()
    print('done')
