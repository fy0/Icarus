from model import db
from model.board import Board
from model.follow import Follow
from model.reply import Reply
from model.test import Test
from model.topic import Topic
from model.user import User
from model.wiki import WikiItem, WikiArticle, WikiHistory

db.connect()
db.create_tables([Test, Board, Follow, Reply, Topic, User, WikiItem, WikiArticle, WikiHistory], safe=True)
