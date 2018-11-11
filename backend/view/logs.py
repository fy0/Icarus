from model.manage_log import ManageLog
from slim.base.permission import Permissions
from slim.support.peewee import PeeweeView
from view import route
from permissions import permissions_add_all


@route('log/manage')
class LogManageView(PeeweeView):
    model = ManageLog

    @classmethod
    def ready(cls):
        cls.add_soft_foreign_key('user_id', 'user')

    @classmethod
    def permission_init(cls):
        permission: Permissions = cls.permission
        permissions_add_all(permission)
