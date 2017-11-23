import time
import config
from typing import Dict
from model.comment import Comment
from slim.base.view import ParamsQueryInfo
from slim.retcode import RETCODE
from slim.support.peewee import PeeweeView
from slim.utils import to_bin
from view import route, ValidateForm
from wtforms import validators as va, StringField, IntegerField
from view.user import UserMixin


@route('comment')
class CommentView(UserMixin, PeeweeView):
    model = Comment
