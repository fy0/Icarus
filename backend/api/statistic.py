from api.view.curd import BaseCrudUserView
from app import app
from crud.schemas.post_stats import PostStats


@app.route.view('stats', None)
class StatsView(BaseCrudUserView):
    model = PostStats

    @classmethod
    def ready(cls):
        cls.add_soft_foreign_key('last_comment_id', 'comment')
        cls.add_soft_foreign_key('last_edit_user_id', 'user')
