from crud.roles.r10_vistor import visitor
from crud.roles.r11_banned_user import banned_user
from crud.roles.r20_inactive_user import inactive_user
from crud.roles.r30_normal_user import normal_user
from crud.roles.r31_wiki_editor import wiki_editor
from crud.roles.r40_super_user import super_user
from crud.roles.r50_admin import admin
from crud.schemas.board import Board
from crud.schemas.comment import Comment
from crud.schemas.manage_log import ManageLog
from crud.schemas.notif import Notification
from crud.schemas.post_stats import PostStats
from crud.schemas.topic import Topic
from crud.schemas.upload import Upload
from crud.schemas.user import User
from crud.schemas.wiki_article import WikiArticle
from model import db
from model.board_model import BoardModel
from model.comment_model import CommentModel
from model.manage_log import ManageLogModel
from model.notif import NotificationModel
from model.post_stats import PostStatsModel
from model.topic_model import TopicModel
from model.upload_model import UploadModel
from model.user_model import UserModel
from model.wiki import WikiArticleModel
from pycurd.crud.ext.peewee_crud import PeeweeCrud


c = PeeweeCrud({
    None: visitor,
    'banned_user': banned_user,
    'inactive_user': inactive_user,
    'normal_user': normal_user,
    'wiki_editor': wiki_editor,
    'super_user': super_user,
    'admin': admin
}, {
    User: UserModel,
    Topic: TopicModel,
    Board: BoardModel,
    Comment: CommentModel,
    ManageLog: ManageLogModel,
    Notification: NotificationModel,
    PostStats: PostStatsModel,
    Upload: UploadModel,
    WikiArticle: WikiArticleModel,
}, db)
