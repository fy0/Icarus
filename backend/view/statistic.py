from model.comment import Comment
from model.post_stats import PostStats
from slim.base.permission import Permissions
from slim.support.peewee import PeeweeView
from view import route, ValidateForm
from permissions import permissions_add_all
from view.user import UserMixin


@route('stats', None)
class StatsView(UserMixin, PeeweeView):
    model = PostStats

    @classmethod
    def ready(cls):
        cls.add_soft_foreign_key('last_comment_id', 'comment')
        cls.add_soft_foreign_key('last_edit_user_id', 'user')

    @classmethod
    def permission_init(cls):
        permission: Permissions = cls.permission
        permissions_add_all(permission)
