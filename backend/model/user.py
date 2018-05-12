import hmac
import os
import time
from peewee import *
import config
from model._post import PostModel
from slim.base.user import BaseUser
from slim.utils import StateObject
from model import BaseModel, MyTimestampField, CITextField, db, SerialField


class USER_GROUP(StateObject):
    BAN = 10
    INACTIVE = 40
    NORMAL = 50
    SUPERUSER = 90
    ADMIN = 100

    txt = {BAN: '封禁', INACTIVE: '未激活', NORMAL: '会员', SUPERUSER: '超级用户', ADMIN: '管理'}


def get_user_count_seq():
    return db.execute_sql("select nextval('user_count_seq')").fetchone()[0]


class User(PostModel, BaseUser):
    email = TextField(index=True, unique=True)
    nickname = CITextField(index=True, unique=True)  # CITextField
    password = BlobField()
    salt = BlobField()  # auto
    biology = TextField(null=True)  # 简介

    # level = IntegerField(index=True)  # 用户级别
    group = IntegerField(index=True)  # 用户权限组

    key = BlobField(index=True, null=True)
    key_time = MyTimestampField()

    phone = TextField(null=True, default=None)  # 大陆地区
    number = IntegerField(default=get_user_count_seq)  # 序号，第N个用户 sequence='user_count_seq'
    credit = IntegerField(default=0)  # 积分，会消费
    reputation = IntegerField(default=0)  # 声望，不会消失

    class Meta:
        db_table = 'user'

    #object_type = OBJECT_TYPES.USER

    @property
    def roles(self):
        if self.group == USER_GROUP.ADMIN:
            return [None, 'user', 'admin']
        return [None, 'user']

    @classmethod
    def gen_id(cls):
        return config.POST_ID_GENERATOR()

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

    def refresh_key(self):
        count = 0
        while count < 10:
            with db.atomic():
                try:
                    k = self.gen_key()
                    self.key = k['key']
                    self.key_time = k['key_time']
                    self.save()
                    return k
                except DatabaseError:
                    count += 1
                    db.rollback()
        raise ValueError("generate key failed")

    @classmethod
    def get_by_key(cls, key):
        try:
            return cls.get(cls.key == key)
        except DoesNotExist:
            return None

    def set_password(self, new_password):
        info = self.gen_password_and_salt(new_password)
        self.salt = info['salt']
        self.password = info['password']
        self.save()

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

    def __repr__(self):
        return '<User id:%x nickname:%r>' % (int.from_bytes(self.id.tobytes(), 'big'), self.nickname)
