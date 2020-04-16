from app import app
from model.comment import Comment
from model.post_stats import PostStats
from slim.base.permission import Permissions
from slim.support.peewee import PeeweeView
from api import ValidateForm
from api.user import UserViewMixin


@app.route.view('stats', None)
class StatsView(UserViewMixin, PeeweeView):
    model = PostStats

    @classmethod
    def ready(cls):
        cls.add_soft_foreign_key('last_comment_id', 'comment')
        cls.add_soft_foreign_key('last_edit_user_id', 'user')
