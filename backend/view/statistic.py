from model.comment import Comment
from model.statistic import Statistic, Statistic24h
from slim.base.permission import Permissions
from slim.support.peewee import PeeweeView
from view import route, ValidateForm
from wtforms import validators as va, StringField, IntegerField, ValidationError

from view.permissions import visitor, normal_user, admin
from view.user import UserMixin


@route('statistic', None)
class StatisticView(UserMixin, PeeweeView):
    model = Statistic

    @classmethod
    def ready(cls):
        cls.add_soft_foreign_key('last_comment_id', 'comment')

    @classmethod
    def permission_init(cls):
        permission: Permissions = cls.permission
        permission.add(visitor)
        permission.add(normal_user)
        permission.add(admin)


@route('statistic24h', None)
class Statistic24hView(UserMixin, PeeweeView):
    model = Statistic24h

    @classmethod
    def permission_init(cls):
        permission: Permissions = cls.permission
        permission.add(visitor)
        permission.add(normal_user)
        permission.add(admin)
