import traceback
import peewee

from model import db, BaseModel
from model.board import Board
from model.follow import Follow
from model.comment import Comment
from model.manage_log import ManageLog
from model.mention import Mention
from model.notif import Notification, UserNotifLastInfo
from model.post_stats import PostStats, StatsLog
from model.test import Test
from model.topic import Topic
from model.upload import Upload
from model.user import User
from model.user_oauth import UserOAuth
from model.user_token import UserToken
from model.wiki import WikiArticle


def sql_execute(sql):
    try:
        db.execute_sql(sql)
    except Exception as e:
        db.rollback()


def reset():
    sql_execute("""
    DROP TABLE IF EXISTS "board";
    DROP TABLE IF EXISTS "comment";
    DROP TABLE IF EXISTS "follow";
    DROP TABLE IF EXISTS "notif";
    DROP TABLE IF EXISTS "post_stats";
    DROP TABLE IF EXISTS "stats_log";
    DROP TABLE IF EXISTS "topic";
    DROP TABLE IF EXISTS "user";
    DROP TABLE IF EXISTS "user_notif_record";
    DROP TABLE IF EXISTS "user_oauth";
    DROP TABLE IF EXISTS "notif";
    DROP TABLE IF EXISTS "user_notif_last_info";
    DROP TABLE IF EXISTS "wiki_history";
    DROP TABLE IF EXISTS "wiki_item";
    DROP TABLE IF EXISTS "wiki_article";

    DROP SEQUENCE IF EXISTS "id_gen_seq";
    DROP SEQUENCE IF EXISTS "user_count_seq";
    """)


def work():
    try:
        db.execute_sql(r"""
        CREATE OR REPLACE FUNCTION int2bytea(v_number bigint) RETURNS bytea AS $$
        DECLARE
            v_str text;
        BEGIN
            v_str = to_hex(v_number)::text;
            return decode(concat(repeat('0', length(v_str) %% 2), v_str), 'hex');
        END;
        $$ LANGUAGE plpgsql;
        CREATE SEQUENCE IF NOT EXISTS id_gen_seq NO MINVALUE NO MAXVALUE START 4096 NO CYCLE; /* 0x1000 */
        CREATE SEQUENCE IF NOT EXISTS user_count_seq NO MINVALUE NO MAXVALUE START 1 NO CYCLE;
            """)

        # 请注意，这俩需要数据库的 superuser 权限，因此普通用户是做不到的
        # 会提示 permission denied to create extension "hstore" 这样的错误
        # db.execute_sql("""
        # CREATE EXTENSION IF NOT EXISTS hstore;
        # CREATE EXTENSION IF NOT EXISTS citext;
        # """)
    except peewee.ProgrammingError as e:
        db.rollback()
        traceback.print_exc()
        quit()

    sql_execute('alter table "user" drop column key')
    sql_execute('alter table "user" drop column key_time')

    sql_execute('alter table "upload" add column filename text')
    sql_execute('alter table "upload" add column source text')


db.connect()
work()

db.create_tables([Test, Board, Follow, Comment, Topic, User,
                  WikiArticle,
                  Notification, UserNotifLastInfo,
                  UserOAuth,
                  UserToken,
                  Upload,
                  ManageLog,
                  Mention,
                  PostStats,
                  StatsLog], safe=True)

work()

sql_execute("""
ALTER TABLE "board" ALTER COLUMN "id" SET DEFAULT int2bytea(nextval('id_gen_seq')::bigint);
ALTER TABLE "topic" ALTER COLUMN "id" SET DEFAULT int2bytea(nextval('id_gen_seq')::bigint);
ALTER TABLE "user" ALTER COLUMN "id" SET DEFAULT int2bytea(nextval('id_gen_seq')::bigint);
ALTER TABLE "user" ALTER COLUMN "number" SET DEFAULT nextval('user_count_seq')::bigint;
""")

WikiArticle.get_sidebar_article()
WikiArticle.get_main_page_article()
