from model import db
from model.board import Board
from model.follow import Follow
from model.comment import Comment
from model.statistic import Statistic, Statistic24h
from model.test import Test
from model.topic import Topic
from model.user import User
from model.wiki import WikiItem, WikiArticle, WikiHistory

db.connect()

db.execute_sql("""
CREATE EXTENSION IF NOT EXISTS hstore;
CREATE EXTENSION IF NOT EXISTS citext;
""")

db.create_tables([Test, Board, Follow, Comment, Topic, User,
                  WikiItem, WikiArticle, WikiHistory,
                  Statistic, Statistic24h], safe=True)
