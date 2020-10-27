import hashlib
import hmac
import os
import time
import traceback
from typing import Union, Optional

import peewee
from peewee import *
from playhouse.postgres_ext import ArrayField
import config
from lib.utils import get_today_start_timestamp
from model._post import PostModel, POST_STATE, POST_TYPES
from model.manage_log import ManageLogModel
from model.redis import redis, RK_USER_ACTCODE_BY_USER_ID, RK_USER_RESET_KEY_BY_USER_ID, \
    RK_USER_LAST_REQUEST_RESET_KEY_BY_USER_ID, RK_USER_REG_CODE_BY_EMAIL, \
    RK_USER_REG_CODE_AVAILABLE_TIMES_BY_EMAIL, RK_USER_REG_PASSWORD
from slim.base.user import BaseUser
from slim.utils import StateObject, to_hex, to_bin, get_bytes_from_blob
from model import BaseModel, MyTimestampField, CITextField, db, INETField, SerialField


class USER_GROUP(StateObject):
    BAN = 10
    INACTIVE = 40
    NORMAL = 50
    SUPERUSER = 90
    ADMIN = 100

    GROUP_TO_ROLE = {
        BAN: 'ban',
        INACTIVE: 'inactive_user',
        NORMAL: 'user',
        SUPERUSER: 'superuser',
        ADMIN: 'admin'
    }
    txt = {BAN: '封禁', INACTIVE: '未激活', NORMAL: '会员', SUPERUSER: '管理', ADMIN: '超管'}


# 主要用户角色序列
MAIN_ROLE_ORDER = ['admin', 'superuser', 'user', 'inactive_user', 'banned_user', None]


class UserModel(PostModel, BaseUser):
    email = TextField(index=True, unique=True, null=True, default=None)
    phone = TextField(index=True, unique=True, null=True, default=None)  # 大陆地区
    nickname = CITextField(index=True, unique=True, null=True, help_text='用户昵称')  # CITextField
    password = BlobField()
    salt = BlobField()  # auto
    biology = TextField(null=True)  # 简介
    avatar = TextField(null=True)
    type = IntegerField(default=0)  # 账户类型，0默认，1组织
    url = TextField(null=True)  # 个人主页
    location = TextField(null=True)  # 所在地

    # level = IntegerField(index=True)  # 用户级别
    group = IntegerField(index=True, default=USER_GROUP.NORMAL)  # 用户权限组

    is_wiki_editor = BooleanField(default=False, index=True)  # 是否为wiki编辑
    is_board_moderator = BooleanField(default=False, index=True)  # 是否为版主
    is_forum_master = BooleanField(default=False, index=True)  # 超版

    access_time = MyTimestampField(null=True, default=None)  # 最后访问时间，以misc为准吧
    last_check_in_time = MyTimestampField(null=True, default=None)  # 上次签到时间
    check_in_his = IntegerField(default=0)  # 连续签到天数

    number = SerialField()  # 序号，第N个用户，注意这有个问题是不能写sequence='user_count_seq'，应该是peewee的bug
    credit = IntegerField(default=0)  # 积分，会消费
    exp = IntegerField(default=0)  # 经验值，不会消失
    repute = IntegerField(default=0)  # 声望
    ip_registered = INETField(default=None, null=True)  # 注册IP

    # ref_github = TextField(null=True)
    # ref_zhihu = TextField(null=True)
    # ref_weibo = TextField(null=True)

    is_new_user = BooleanField(default=True)  # 是否全新用户（刚注册，未经过修改昵称）
    phone_verified = BooleanField(default=False)  # 手机号已确认
    change_nickname_chance = IntegerField(default=0, help_text='改名机会数量')  # 改名机会数量
    reset_key = BlobField(index=True, null=True, default=None, help_text='重置密码所用key')  # 重置密码所用key

    class Meta:
        db_table = 'user'

    #object_type = OBJECT_TYPES.USER

    @classmethod
    def new(cls, nickname, password, extra_values=None, *, auto_nickname=False, is_for_tests=True) -> Optional[
        'UserModel']:
        values = {
            'nickname': nickname,
            'is_new_user': True
            # 'is_for_tests': is_for_tests
        }

        values.update(extra_values)
        cls.append_post_id(values)

        info = cls.gen_password_and_salt(password)
        values.update(info)

        try:
            uid = cls.insert(values).execute()
            u: UserModel = cls.get_by_pk(uid)

            uchanged = False
            # 如果是第一个用户，那么自动为管理员
            if u.number == 1:
                u.group = USER_GROUP.ADMIN
                uchanged = True

            # 注册成功后，如果要求自动设置用户名，那么修改用户名
            if auto_nickname:
                nprefix = config.USER_NICKNAME_AUTO_PREFIX + '_'
                u.change_nickname_chance = 1
                u.nickname = nprefix + uid.to_hex()
                uchanged = True

            if uchanged:
                u.save()

            return u
        except peewee.IntegrityError:
            traceback.print_exc()
            db.rollback()
            # if e.args[0].startswith('duplicate key | 错误:  重复键违反唯一约束'):
            #     return
            # 此处似乎无从得知，数据库会返回什么样的文本，应该是和语言相关
            # 那么姑且假定 IntegrityError 都是唯一性约束
        except peewee.DatabaseError:
            db.rollback()

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
    def main_role(self):
        """ 主要用户角色 """
        roles = set(self.roles)
        for i in MAIN_ROLE_ORDER:
            if i in roles: return i

    @property
    def roles(self):
        """
        这里角色权限由低到高
        :return:
        """
        ret = [None]
        if self.state == POST_STATE.DEL:
            return ret
        if self.group >= USER_GROUP.BAN:
            ret.append('banned_user')
        if self.group >= USER_GROUP.INACTIVE:
            ret.append('inactive_user')
        if self.group >= USER_GROUP.NORMAL:
            ret.append('user')
        if self.is_wiki_editor:
            ret.append('wiki_editor')
        if self.is_board_moderator:
            ret.append('board_moderator')
        if self.is_forum_master:
            ret.append('forum_master')
        if self.group >= USER_GROUP.SUPERUSER:
            ret.append('superuser')
        if self.group >= USER_GROUP.ADMIN:
            ret.append('admin')
        return ret

    @classmethod
    def gen_password_and_salt(cls, password_text):
        salt = os.urandom(32)
        dk = hashlib.pbkdf2_hmac(
            config.PASSWORD_SECURE_HASH_FUNC_NAME,
            password_text.encode('utf-8'),
            salt,
            config.PASSWORD_SECURE_HASH_ITERATIONS,
        )
        return {'password': dk, 'salt': salt}

    @classmethod
    def get_by_key(cls, key):
        try:
            return cls.get(cls.key == key)
        except DoesNotExist:
            return None

    @classmethod
    async def gen_reg_code_by_email(cls, email: str, password: str):
        t = int(time.time())
        code = os.urandom(8)
        email = email.encode('utf-8')
        pipe = redis.pipeline()
        pipe.set(RK_USER_REG_CODE_AVAILABLE_TIMES_BY_EMAIL % email,
                 config.USER_REG_CODE_AVAILABLE_TIMES_BY_EMAIL,
                 expire=config.USER_REG_CODE_EXPIRE)
        pipe.set(RK_USER_REG_CODE_BY_EMAIL % email, code, expire=config.USER_REG_CODE_EXPIRE)
        pipe.set(RK_USER_REG_PASSWORD % email, password, expire=config.USER_REG_CODE_EXPIRE)
        await pipe.execute()
        return code

    @classmethod
    async def reg_code_cleanup(cls, email):
        email = email.encode('utf-8')
        pipe = redis.pipeline()
        pipe.delete(RK_USER_REG_CODE_BY_EMAIL % email)
        pipe.delete(RK_USER_REG_CODE_AVAILABLE_TIMES_BY_EMAIL % email)
        pipe.delete(RK_USER_REG_PASSWORD % email)
        await pipe.execute()

    @classmethod
    async def check_reg_code_by_email(cls, email, code: Union[str, bytes]):
        """
        检查账户激活码是否可用
        :param uid:
        :param code:
        :return:
        """
        if not code: return
        if isinstance(code, str): code = to_bin(code)

        if len(code) == 8:
            email_bytes = email.encode('utf-8')
            rk_code = RK_USER_REG_CODE_BY_EMAIL % email_bytes
            rk_times = RK_USER_REG_CODE_AVAILABLE_TIMES_BY_EMAIL % email_bytes
            rk_pw = RK_USER_REG_PASSWORD % email_bytes

            if await redis.get(rk_code) == code:
                # 检查可用次数，decr的返回值是执行后的
                if int(await redis.decr(rk_times)) <= 0:
                    return await cls.reg_code_cleanup(email)
                # 无问题，取出储存值
                return (await redis.get(rk_pw)).decode('utf-8')

    async def can_request_reset_password(self):
        """
        是否能申请重置密码
        :return:
        """
        val = await redis.get(RK_USER_LAST_REQUEST_RESET_KEY_BY_USER_ID % self.id)
        if val is None:
            return True
        if time.time() - int(val) > config.USER_RESET_PASSWORD_CODE_EXPIRE:
            return True

    def gen_reset_key(self) -> bytes:
        """
        生成一个重置密码key
        :return:
        """
        # len == 16 + 8 == 24
        t = int(time.time())
        code = os.urandom(16) + t.to_bytes(8, 'little')
        redis.set(RK_USER_LAST_REQUEST_RESET_KEY_BY_USER_ID % self.id, t, expire=config.USER_RESET_PASSWORD_REQUST_INTERVAL)
        redis.set(RK_USER_RESET_KEY_BY_USER_ID % self.id, code, expire=config.USER_RESET_PASSWORD_CODE_EXPIRE)
        return code

    @classmethod
    async def check_reset_key(cls, uid, code) -> Union['UserModel', None]:
        """
        检查uid与code这一组密码重置密钥是否有效
        :param uid:
        :param code:
        :return:
        """
        if not code: return
        if isinstance(uid, str): uid = to_bin(uid)
        if isinstance(code, str): code = to_bin(code)

        if len(code) == 24:
            rkey = RK_USER_RESET_KEY_BY_USER_ID % uid
            if await redis.get(rkey) == code:
                try:
                    u = cls.get(cls.id == uid)
                    await redis.delete(rkey)
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
            if old_time > last_midnight - config.USER_CHECKIN_COUNTER_INTERVAL:
                self.check_in_his += 1
            else:
                self.check_in_his = 1
            self.save()

            # 签到加分
            credit = self.credit
            exp = self.exp
            self.credit += 5
            self.exp += 5
            self.save()

            ManageLogModel.add_by_credit_changed_sys(get_bytes_from_blob(self.id), credit, self.credit, note='每日签到')
            ManageLogModel.add_by_exp_changed_sys(get_bytes_from_blob(self.id), exp, self.exp, note='每日签到')

            return {
                'credit': 5,
                'exp': 5,
                'time': self.last_check_in_time,
                'check_in_his': self.check_in_his
            }

    def daily_access_reward(self):
        self.access_time = self.access_time or 0
        old_time = self.access_time
        self.update_access_time()

        if old_time < get_today_start_timestamp():
            exp = self.exp
            self.exp += 5
            self.save()
            ManageLogModel.add_by_exp_changed_sys(get_bytes_from_blob(self.id), exp, self.exp, note='每日登录')
            return {'exp': 5}

    def _auth_base(self, password_text):
        """
        已获取了用户对象，进行密码校验
        :param password_text:
        :return:
        """
        dk = hashlib.pbkdf2_hmac(
            config.PASSWORD_SECURE_HASH_FUNC_NAME,
            password_text.encode('utf-8'),
            get_bytes_from_blob(self.salt),
            config.PASSWORD_SECURE_HASH_ITERATIONS,
        )

        if get_bytes_from_blob(self.password) == dk:
            return self

    @classmethod
    def auth_by_mail(cls, email, password_text) -> ["UserModel", bool]:
        try: u = cls.get(cls.email == email)
        except DoesNotExist: return None, False
        return u, u._auth_base(password_text)

    @classmethod
    def auth_by_username(cls, username, password_text) -> ["UserModel", bool]:
        try: u = cls.get(cls.username == username)
        except DoesNotExist: return None, False
        return u, u._auth_base(password_text)

    def __repr__(self):
        return '<User id:%x nickname:%r>' % (int.from_bytes(get_bytes_from_blob(self.id), 'big'), self.nickname)

    @classmethod
    def get_post_type(cls):
        return POST_TYPES.USER

    def get_title(self):
        return self.nickname
