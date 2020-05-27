import hashlib
import json
import os

from aiohttp.web_request import FileField
from slim.ext.decorator import require_role

import config
from app import app
from model.upload import Upload
from model.user import User
from slim.base.permission import Permissions
from slim.retcode import RETCODE
from slim.support.peewee import PeeweeView
from slim.utils import binhex, CustomID
from api.user import UserViewMixin


upload_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', config.UPLOAD_DIR))
os.makedirs(upload_dir, exist_ok=True)


@app.route.view('upload')
class UploadView(UserViewMixin, PeeweeView):
    model = Upload

    @app.route.interface('POST')
    # @require_role(USER_ROLE)
    async def upload(self):
        """
        上传图片
        随机文件名，上传至指定目录。完成后修改文件名为hash值
        :return:
        """
        size = 0
        cid = CustomID()
        user: User = self.current_user
        fn = os.path.join(upload_dir, str(cid.to_hex()))
        m = hashlib.blake2b()

        post = await self.post_data()
        field: FileField = post.get('file', None)

        if not (field and isinstance(field, FileField)):
            return self.finish(RETCODE.INVALID_POSTDATA, '没有提交 file 字段，或字段内容不是一个文件')

        with open(fn, 'wb') as f:
            while True:
                chunk = field.file.read(8192)  # 8192 bytes by default.
                if not chunk:
                    break
                size += len(chunk)
                f.write(chunk)
                m.update(chunk)

        key = m.hexdigest()
        if not Upload.get_by_key(key):
            # 如果不存在，那么改名为hash值
            os.rename(fn, os.path.join(upload_dir, key))
        else:
            # 如果已存在，那么删除
            os.remove(fn)

        upload = Upload.new_with_user(user.id, m.digest(), field.filename, size)
        self.finish(RETCODE.SUCCESS, upload.to_dict())

    @app.route.interface('POST')
    async def qn_token(self):
        """
        获取七牛 token
        :return:
        """
        from lib import qn
        user = self.current_user
        if user:
            if self.current_request_role in ('user', 'admin', 'superuser'):
                type_name = 'avatar' if self.params.get('is_avatar', False) else None
                return self.finish(RETCODE.SUCCESS, qn.get_token(user.id.hex(), type_name))
        self.finish(RETCODE.FAILED)

    @app.route.interface('POST')
    async def qn_callback(self):
        """
        七牛回调
        :return:
        """
        from lib import qn
        ua = self.headers.get('User-Agent', None)
        if not (ua and ua.startswith('qiniu-callback')):
            return self.finish(RETCODE.FAILED)

        auth = self.headers.get('Authorization', None)
        if auth:
            content = str(await self._request.content.read(), 'utf-8')
            if qn.verify_callback(auth, str(self._request.url), content):
                # 鉴权成功，确认为七牛服务器回调
                info = json.loads(content)
                uid = binhex.to_bin(info['user_id'])
                # 说明一下，这个哈希值不是base64 hex等编码，具体比较奇怪看了就知道了
                # 总之因此直接使用了TextField来存放
                key = info['key']
                Upload.new(uid, key, info['size'], info['ext'], info['type_name'], info['image_info'])
                if info['type_name'] == 'avatar':
                    # 更换用户头像
                    u = User.get_by_pk(uid)
                    if u:
                        u.avatar = key
                        u.save()
                return self.finish(RETCODE.SUCCESS, key)

        self.finish(RETCODE.FAILED)
