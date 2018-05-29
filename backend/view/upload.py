from lib import upload
from model.upload import Upload
from slim.base.permission import Permissions
from slim.retcode import RETCODE
from slim.support.peewee import PeeweeView
from view import route
from view.permissions import permissions_add_all
from view.user import UserMixin


@route('upload')
class TopicView(UserMixin, PeeweeView):
    model = Upload

    @route.interface('POST')
    async def token(self):
        user = self.current_user
        if user:
            if self.current_role in ('user', 'admin', 'superuser'):
                return self.finish(RETCODE.SUCCESS, upload.get_token(user.id.hex()))
        self.finish(RETCODE.FAILED)

    @classmethod
    def ready(cls):
        cls.add_soft_foreign_key('hash', 'upload_entity')

    @classmethod
    def permission_init(cls):
        permission: Permissions = cls.permission
        permissions_add_all(permission)
