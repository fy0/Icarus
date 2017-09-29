import hmac
import os

import time
from peewee import *

import config
from slim.base.permission import BaseUser
from slim.utils import StateObject
from model import BaseModel


class USER_GROUP(StateObject):
    BAN = 10
    INACTIVE = 40
    NORMAL = 50
    ADMIN = 100

    txt = {BAN: '封禁', INACTIVE: '未激活', NORMAL: '会员', ADMIN: '管理'}


class USER_STATE(StateObject):
    DEL = 0
    NORMAL = 50

    txt = {DEL: '删除', NORMAL: '正常'}


class User(BaseModel, BaseUser):
    id = BlobField(primary_key=True)
    email = CharField(index=True, max_length=128)
    nickname = CharField(index=True, max_length=32, null=True, default=None)
    password = BlobField()
    salt = BlobField()  # auto

    group = IntegerField(index=True)  # 用户组
    state = IntegerField(index=True)

    key = BlobField(index=True)
    key_time = BigIntegerField()
    reg_time = BigIntegerField()

    class Meta:
        db_table = 'user'

    #object_type = OBJECT_TYPES.USER

    @property
    def roles(self):
        return [None, 'user']

    @classmethod
    def gen_id(cls):
        return config.ID_GENERATOR()

    @classmethod
    def gen_password_and_salt(cls, password_text):
        salt = os.urandom(16)
        m = hmac.new(salt, digestmod=config.PASSWORD_HASH_FUNC)
        m.update(password_text.encode('utf-8'))
        return {'password': m.digest(), 'salt': salt}

    @classmethod
    def gen_key(cls):
        key = os.urandom(16)
        key_time = int(time.time())
        return {'key': key, 'key_time': key_time}

    @classmethod
    def get_by_key(cls, key):
        try:
            return cls.get(cls.key == key)
        except DoesNotExist:
            return None

    @classmethod
    def auth(cls, email, password_text):
        try:
            u = cls.get(cls.email == email)
        except DoesNotExist:
            return False

        m = hmac.new(u.salt.tobytes(), digestmod=config.PASSWORD_HASH_FUNC)
        m.update(password_text.encode('utf-8'))

        if u.password.tobytes() == m.digest():
            return u
