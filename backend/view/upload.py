import json

from lib import upload
from model.user_upload import UserUpload
from slim.base.permission import Permissions
from slim.retcode import RETCODE
from slim.support.peewee import PeeweeView
from view import route
from view.permissions import permissions_add_all
from view.user import UserMixin


@route('upload')
class TopicView(UserMixin, PeeweeView):
    model = UserUpload

    @route.interface('POST')
    async def token(self):
        user = self.current_user
        if user:
            if self.current_role in ('user', 'admin', 'superuser'):
                type_name = 'avatar' if self.params.get('is_avatar', False) else None
                return self.finish(RETCODE.SUCCESS, upload.get_token(user.id.hex(), type_name))
        self.finish(RETCODE.FAILED)

    @route.interface('POST')
    async def qn_callback(self):
        ua = self.headers.get('User-Agent', None)
        if not (ua and ua.startswith('qiniu-callback')):
            return self.finish(RETCODE.FAILED)

        auth = self.headers.get('Authorization', None)
        if auth:
            content = str(await self._request.content.read(), 'utf-8')
            if upload.verify_callback(auth, str(self._request.url), content):
                # 鉴权成功，确认为七牛服务器回调
                info = json.loads(content)
                UserUpload.new(info['user_id'], info['key'], info['size'],
                               info['ext'], info['type_name'], info['image_info'])
                return self.finish(RETCODE.SUCCESS)

        self.finish(RETCODE.FAILED)

    @classmethod
    def ready(cls):
        pass

    @classmethod
    def permission_init(cls):
        permission: Permissions = cls.permission
        permissions_add_all(permission)
