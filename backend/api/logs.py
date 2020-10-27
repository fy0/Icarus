from api.view.curd import BaseCrudUserView
from app import app
from crud.schemas.manage_log import ManageLog


@app.route.view('log/manage')
class LogManageView(BaseCrudUserView):
    model = ManageLog

    @classmethod
    def ready(cls):
        cls.add_soft_foreign_key('user_id', 'user')
