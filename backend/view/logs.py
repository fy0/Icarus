from model.log_manage import ManageLog
from slim.base.permission import Permissions
from slim.support.peewee import PeeweeView
from view import route
from view.permissions import visitor, normal_user, super_user, admin


@route('log/manage')
class LogManageView(PeeweeView):
    model = ManageLog

    @classmethod
    def ready(cls):
        cls.add_soft_foreign_key('user_id', 'user')

    @classmethod
    def permission_init(cls):
        permission: Permissions = cls.permission
        permission.add(visitor)
        permission.add(normal_user)
        permission.add(super_user)
        permission.add(admin)
