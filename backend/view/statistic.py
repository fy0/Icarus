from model.comment import Comment
from model.post_stats import PostStats
from slim.base.permission import Permissions
from slim.support.peewee import PeeweeView
from view import route, ValidateForm
from view.user import UserViewMixin


@route('stats', None)
class StatsView(UserViewMixin, PeeweeView):
    model = PostStats

    @classmethod
    def ready(cls):
        cls.add_soft_foreign_key('last_comment_id', 'comment')
        cls.add_soft_foreign_key('last_edit_user_id', 'user')
