import peewee

from model import db, BaseModel
from model.board import Board
from model.follow import Follow
from model.comment import Comment
from model.notif import Notification, UserNotifRecord
from model.statistic import Statistic, Statistic24h
from model.test import Test
from model.topic import Topic
from model.user import User
from model.wiki import WikiItem, WikiArticle, WikiHistory

db.connect()


def reset():
    db.execute_sql("""
    DROP TABLE IF EXISTS "board";
    DROP TABLE IF EXISTS "comment";
    DROP TABLE IF EXISTS "follow";
    DROP TABLE IF EXISTS "notif";
    DROP TABLE IF EXISTS "statistic";
    DROP TABLE IF EXISTS "statistic24h";
    DROP TABLE IF EXISTS "topic";
    DROP TABLE IF EXISTS "user";
    DROP TABLE IF EXISTS "user_notif_record";
    DROP TABLE IF EXISTS "wiki_history";
    DROP TABLE IF EXISTS "wiki_item";
    DROP TABLE IF EXISTS "wiki_article";

    DROP SEQUENCE IF EXISTS id_gen_seq;
    DROP SEQUENCE IF EXISTS user_count_seq;
    """)


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
    CREATE SEQUENCE IF NOT EXISTS id_gen_seq NO MINVALUE NO MAXVALUE START 1000 CACHE 1000 NO CYCLE;
    CREATE SEQUENCE IF NOT EXISTS user_count_seq NO MINVALUE NO MAXVALUE START 1 CACHE 1000 NO CYCLE;
        """)

    db.execute_sql("""
    CREATE EXTENSION IF NOT EXISTS hstore;
    CREATE EXTENSION IF NOT EXISTS citext;
    """)
except peewee.ProgrammingError:
    # permission denied to create extension "hstore"
    db.rollback()

db.create_tables([Test, Board, Follow, Comment, Topic, User,
                  WikiItem, WikiArticle, WikiHistory,
                  Notification, UserNotifRecord,
                  Statistic, Statistic24h], safe=True)


try:
    db.execute_sql("""
ALTER TABLE "board" ALTER COLUMN "id" SET DEFAULT int2bytea(nextval('id_gen_seq')::bigint);
ALTER TABLE "topic" ALTER COLUMN "id" SET DEFAULT int2bytea(nextval('id_gen_seq')::bigint);
ALTER TABLE "user" ALTER COLUMN "id" SET DEFAULT int2bytea(nextval('id_gen_seq')::bigint);
    """)

except peewee.ProgrammingError:
    db.rollback()
