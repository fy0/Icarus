"""
token
fingerprint
useragent
expire_time
ip
"""
import binascii
import os
import time
from typing import Optional

import peewee
from peewee import TextField, BigIntegerField, BlobField
from slim.utils import to_bin, get_bytes_from_blob

from model import StdUserModel, INETField, db


class UserToken(StdUserModel):
    expire = BigIntegerField(null=True)

    first_meet_time = BigIntegerField(null=True)
    ip_first_meet = INETField(default=None, null=True)  # 注册IP
    ua_first_meet = TextField(null=True)

    last_access_time = BigIntegerField(null=True)
    ip_latest = INETField(default=None, null=True)
    ua_latest = TextField(null=True)

    class Meta:
        db_table = 'user_token'

    @classmethod
    def new(cls, user_id, expires_days=30):
        create_time = int(time.time())
        expire_time = create_time + expires_days * 24 * 60 * 60
        token = os.urandom(16)
        return UserToken.create(id=token, time=create_time, user_id=user_id, expire=expire_time)

    @classmethod
    def clear_by_user_id(cls, user_id):
        try:
            cls.update(deleted_at=int(time.time())).where(cls.user_id == user_id).execute()
        except peewee.DatabaseError:
            db.rollback()

    @classmethod
    def get_by_token(cls, token) -> Optional['UserToken']:
        if isinstance(token, str):
            try:
                token = to_bin(token)
            except binascii.Error:
                return

        try:
            t = cls.get(cls.id == token, time.time() < cls.expire, cls.deleted_at.is_null(True))
        except peewee.DoesNotExist:
            pass

    def get_token(self):
        return get_bytes_from_blob(self.id)

    async def init(self, view: 'AbstractSQLView'):
        """
        从请求初始化信息
        :param view:
        :return:
        """
        # req = view._request
        self.first_meet_time = int(time.time())
        self.ip_first_meet = await view.get_ip()
        self.ua_first_meet = view.headers.get('User-Agent', None)
        self.save()

    async def access_save(self, view: 'AbstractSQLView'):
        self.last_access_time = int(time.time())
        self.ip_latest = await view.get_ip()
        self.ua_latest = view.headers.get('User-Agent', None)
        self.save()
