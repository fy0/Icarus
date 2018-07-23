import hmac
import os
import struct
import time

import binascii
from typing import Union

from peewee import *
import config
from lib.utils import get_today_start_timestamp
from model._post import PostModel
from model.log_manage import ManageLog
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
    avatar = TextField(null=True)
    type = IntegerField(default=0)  # 账户类型，0默认，1组织
    url = TextField(null=True)  # 个人主页
    location = TextField(null=True)  # 所在地

    # level = IntegerField(index=True)  # 用户级别
    group = IntegerField(index=True)  # 用户权限组

    key = BlobField(index=True, null=True)
    key_time = MyTimestampField()  # 最后登录时间
    access_time = MyTimestampField(null=True, default=None)  # 最后访问时间，以misc为准吧
    last_check_in_time = MyTimestampField(null=True, default=None)  # 上次签到时间
    check_in_his = IntegerField(default=0)  # 连续签到天数

    phone = TextField(null=True, default=None)  # 大陆地区
    number = IntegerField(default=get_user_count_seq)  # 序号，第N个用户 sequence='user_count_seq'
    credit = IntegerField(default=0)  # 积分，会消费
    reputation = IntegerField(default=0)  # 声望，不会消失

    reset_key = BlobField(index=True, null=True, default=None)  # 重置密码所用key

    class Meta:
        db_table = 'user'

    #object_type = OBJECT_TYPES.USER

    @classmethod
    def find_by_nicknames(cls, names):
        it = iter(names)
        try:
            condition = cls.nickname == next(it)
        except StopIteration:
            return []
        for i in it:
            condition |= cls.nickname == i
        return cls.select().where(condition)

    @property
    def roles(self):
        ret = [None]
        if self.group >= USER_GROUP.ADMIN:
            ret.append('admin')
        if self.group >= USER_GROUP.SUPERUSER:
            ret.append('superuser')
        if self.group >= USER_GROUP.NORMAL:
            ret.append('user')
        if self.group >= USER_GROUP.INACTIVE:
            ret.append('inactive_user')
        return ret

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

    def get_activation_code(self):
        raw = self.salt.tobytes() + self.time.to_bytes(8, 'little')  # len == 16 + 8 == 24
        return str(binascii.hexlify(raw), 'utf-8')

    @classmethod
    def check_active(cls, uid, code):
        if not code: return
        try:
            uid = binascii.unhexlify(uid)
            code = binascii.unhexlify(code)
        except:
            return

        if len(code) == 24:
            # 时间为最近3天
            ts = int.from_bytes(binascii.unhexlify(code[16:]), 'little')
            if time.time() - ts < 3 * 24 * 60 * 60:
                try:
                    u = cls.get(cls.time == ts,
                                cls.id == uid,
                                cls.group == USER_GROUP.INACTIVE,
                                cls.salt == binascii.unhexlify(code[:16]))
                    u.group = USER_GROUP.NORMAL
                    u.save()
                    return u
                except cls.DoesNotExist:
                    pass

    @staticmethod
    def gen_reset_key():
        return os.urandom(16) + int(time.time()).to_bytes(8, 'little')  # len == 16 + 8 == 24

    @classmethod
    def check_reset(cls, uid, code) -> Union['User', None]:
        if not code: return
        try:
            uid = binascii.unhexlify(uid)
            code = binascii.unhexlify(code)
        except: return

        if len(code) == 24:
            # 时间为最近12小时
            ts = int.from_bytes(code[16:], 'little')
            if time.time() - ts < 12 * 60 * 60:
                try:
                    u = cls.get(cls.id == uid, cls.reset_key == code)
                    return u
                except cls.DoesNotExist:
                    pass

    def set_password(self, new_password):
        info = self.gen_password_and_salt(new_password)
        self.salt = info['salt']
        self.password = info['password']
        self.save()

    def update_access_time(self):
        self.access_time = int(time.time())
        self.save()
        return self.access_time

    def check_in(self):
        self.last_check_in_time = self.last_check_in_time or 0
        old_time = self.last_check_in_time
        last_midnight = get_today_start_timestamp()

        # 今日未签到
        if self.last_check_in_time < last_midnight:
            self.last_check_in_time = int(time.time())
            # 三天内有签到，连击
            print(old_time, last_midnight - 3 * 24 * 60 * 60)
            if old_time > last_midnight - 3 * 24 * 60 * 60:
                self.check_in_his += 1
            else:
                self.check_in_his = 1
            self.save()

            # 签到加分
            credit = self.credit
            reputation = self.reputation
            self.credit += 5
            self.reputation += 5
            self.save()
            ManageLog.add_by_credit_changed_sys(self, note='每日签到', value=[credit, self.credit])
            ManageLog.add_by_reputation_changed_sys(self, note='每日签到', value=[reputation, self.reputation])

            return {
                'credit': 5,
                'reputation': 5,
                'time': self.last_check_in_time,
                'check_in_his': self.check_in_his
            }

    def daily_access_reward(self):
        self.access_time = self.access_time or 0
        old_time = self.access_time
        self.update_access_time()

        if old_time < get_today_start_timestamp():
            credit = self.credit
            self.credit += 5
            self.save()
            ManageLog.add_by_credit_changed_sys(self, note='每日登录', value=[credit, self.credit])
            return 5

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
