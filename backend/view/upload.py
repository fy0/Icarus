from model.upload import Upload
from slim.base.permission import Permissions
from slim.support.peewee import PeeweeView
from view import route
from view.permissions import permissions_add_all
from view.user import UserMixin


@route('upload')
class TopicView(UserMixin, PeeweeView):
    model = Upload

    @classmethod
    def ready(cls):
        cls.add_soft_foreign_key('hash', 'upload_entity')

    @classmethod
    def permission_init(cls):
        permission: Permissions = cls.permission
        permissions_add_all(permission)
