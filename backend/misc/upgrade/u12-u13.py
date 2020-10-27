"""
如果执行失败，请将此文件复制到backend目录再次执行。
"""

import sys
sys.path.insert(0, '.')

import time
import peewee
from model import db
from model._post import POST_STATE
from model.comment_model import CommentModel
from model.manage_log import ManageLogModel, MOP
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
    sql_execute('drop table "wiki_history";')
    sql_execute('drop table "wiki_item";')
    sql_execute('drop table "wiki_article";')
    sql_execute('drop table "statistic24h";')
    sql_execute('drop table "statistic24h_log";')
    sql_execute('ALTER TABLE statistic RENAME TO post_stats;')
    sql_execute('ALTER TABLE post_stats ADD edit_count int DEFAULT 0 NULL;')
    sql_execute('ALTER TABLE post_stats DROP viewed_users;')
    sql_execute('ALTER TABLE post_stats DROP edited_users;')
    sql_execute('ALTER TABLE post_stats DROP commented_users;')
    sql_execute('ALTER TABLE post_stats DROP bookmarked_users;')
    sql_execute('ALTER TABLE post_stats DROP upvoted_users;')
    sql_execute('ALTER TABLE post_stats DROP downvoted_users;')
    sql_execute('ALTER TABLE post_stats DROP thanked_users;')
    sql_execute('ALTER TABLE post_stats ADD last_edit_time bigint DEFAULT NULL NULL;')
    sql_execute('ALTER TABLE post_stats ADD last_edit_user_id BYTEA DEFAULT NULL NULL;')
    sql_execute('CREATE INDEX post_stats_last_edit_time_index ON post_stats (last_edit_time);')
    sql_execute('ALTER TABLE post_stats ADD update_time bigint DEFAULT NULL NULL;')
    sql_execute('CREATE INDEX update_time_index ON post_stats (update_time);')
    sql_execute(r"ALTER TABLE user_notif_last_info ADD last_manage_log_id bytea DEFAULT '\x00' NULL;")
    sql_execute('ALTER TABLE notif ALTER COLUMN from_post_type DROP NOT NULL;')
    sql_execute('ALTER TABLE notif ALTER COLUMN from_post_id DROP NOT NULL;')

    sql_execute('ALTER TABLE "user" ADD is_wiki_editor BOOLEAN DEFAULT FALSE NOT NULL;')
    sql_execute('ALTER TABLE "user" ADD is_board_moderator BOOLEAN DEFAULT FALSE  NOT NULL;')
    sql_execute('ALTER TABLE "user" ADD is_forum_master BOOLEAN DEFAULT FALSE NOT NULL;')
    sql_execute('CREATE INDEX user_is_wiki_editor_index ON "user" (is_wiki_editor);')
    sql_execute('CREATE INDEX user_is_board_moderator_index ON "user" (is_board_moderator);')
    sql_execute('CREATE INDEX user_is_forum_master_index ON "user" (is_forum_master);')

    # 移除 MOP.TOPIC_TITLE_CHANGE 300
    ManageLogModel.update(operation=MOP.POST_TITLE_CHANGE).where(ManageLogModel.operation == 300).execute()
    # 移除 MOP.TOPIC_CONTENT_CHANGE 301
    ManageLogModel.update(operation=MOP.POST_CONTENT_CHANGE).where(ManageLogModel.operation == 301).execute()
    # 移除 MOP.COMMENT_STATE_CHANGE 500
    ManageLogModel.update(operation=MOP.POST_STATE_CHANGE).where(ManageLogModel.operation == 500).execute()

    # BOARD_NEW 200
    for i in ManageLogModel.select().where(ManageLogModel.operation == 200):
        i.operation = MOP.POST_CREATE
        i.value = {'title': i.value}
        i.save()

    for i in ManageLogModel.select():
        if i and i.value:
            if i.operation == MOP.POST_CREATE:
                # wiki 改动
                if not isinstance(i.value, dict):
                    i.value = {'title': i.value}
                    i.save()
            elif isinstance(i.value, list):
                i.value = {'change': i.value}
                i.save()
            elif isinstance(i.value, dict):
                pass
            else:
                if i.operation == MOP.POST_CONTENT_CHANGE:
                    i.value = {'change': i.value}
                    i.save()


if __name__ == '__main__':
    work()
    print('done')
