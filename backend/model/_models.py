import peewee

from model import db
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

try:
    db.execute_sql("""
    CREATE EXTENSION IF NOT EXISTS hstore;
    CREATE EXTENSION IF NOT EXISTS citext;
    """)
except peewee.ProgrammingError:
    # permission denied to create extension "hstore"
    db.rollback()

db.create_tables([Test, Board, Follow, Comment, Topic,
                  WikiItem, WikiArticle, WikiHistory,
                  Notification, UserNotifRecord,
                  Statistic, Statistic24h], safe=True)
