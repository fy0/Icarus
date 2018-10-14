import os
import re
import time
import peewee
import config
from typing import Dict, Type, List
from lib import mail
from model import db
from model.log_manage import ManageLog, MANAGE_OPERATION as MOP
from model.notif import UserNotifLastInfo
from model._post import POST_TYPES, POST_STATE
from model.statistic import statistic_new
from slim.base.sqlquery import SQLValuesToWrite
from slim.base.user import BaseUser, BaseAccessTokenUserMixin
from slim.retcode import RETCODE
from model.user import User, USER_GROUP
from slim.utils import to_hex, to_bin
from view import route, ValidateForm, cooldown, same_user, get_fuzz_ip
from wtforms import StringField, validators as va, ValidationError
from slim.base.permission import Permissions, DataRecord
from permissions import permissions_add_all
from view.user_signup_legacy import UserLegacyView
from view.user_validate_form import RequestSignupByEmailForm, SigninByEmailForm, SigninByNicknameForm, PasswordForm, \
    NicknameForm


class UserMixin(BaseAccessTokenUserMixin):
    def teardown_user_key(self):
        u: User = self.current_user
        u.key = None
        u.save()

    def get_user_by_key(self, key):
        if not key: return
        try: return User.get_by_key(to_bin(key))
        except: pass


class ChangePasswordForm(ValidateForm):
    old_password = StringField('密码', validators=[
        va.required(),
        # va.Length(config.USER_PASSWORD_MIN, config.USER_PASSWORD_MAX)
    ])

    password = StringField('密码', validators=[
        va.required(),
        # va.Length(config.USER_PASSWORD_MIN, config.USER_PASSWORD_MAX)
    ])


class ResetPasswordForm(ValidateForm):
    email = StringField('邮箱', validators=[va.required(), va.Length(3, config.USER_EMAIL_MAX), va.Email()])
    nickname = StringField('昵称', validators=[
        va.required(),
        va.Length(min(config.USER_NICKNAME_CN_FOR_REG_MIN, config.USER_NICKNAME_FOR_REG_MIN), config.USER_NICKNAME_FOR_REG_MAX),
        # nickname_check  # 发生了新旧可用昵称列表不同，然后找回密码出现了“昵称被占用”的情况
    ])


async def same_email_post(view):
    post = await view.post_data()
    if 'email' in post:
        return post['email'].lower().encode('utf-8')


@route('user')
class UserView(UserMixin, UserLegacyView):
    model = User

    @classmethod
    def permission_init(cls):
        permission: Permissions = cls.permission
        permissions_add_all(permission)

    @route.interface('POST')
    @cooldown(config.USER_REQUEST_PASSWORD_RESET_COOLDOWN_BY_IP, b'ic_cd_user_request_reset_password_%b')
    @cooldown(config.USER_REQUEST_PASSWORD_RESET_COOLDOWN_BY_ACCOUNT, b'ic_cd_user_request_reset_password_account_%b', unique_id_func=same_email_post)
    async def request_password_reset(self):
        """
        申请重置密码 / 忘记密码
        :return:
        """
        post = await self.post_data()
        form = ResetPasswordForm(**post)
        if not form.validate():
            return self.finish(RETCODE.FAILED, form.errors)

        try:
            user = User.get(User.nickname == post['nickname'], User.email == post['email'])
        except User.DoesNotExist:
            user = None

        if user:
            if await user.can_request_reset_password():
                key = user.gen_reset_key()
                user.reset_key = key
                user.save()
                await mail.send_password_reset(user)
                self.finish(RETCODE.SUCCESS, {'id': user.id, 'nickname': user.nickname})
            else:
                self.finish(RETCODE.FAILED)
        else:
            self.finish(RETCODE.FAILED)

    @route.interface('POST')
    async def validate_password_reset(self):
        """
        验证忘记密码
        :return:
        """
        post = await self.post_data()
        form = PasswordForm(**post)
        if not form.validate():
            return self.finish(RETCODE.FAILED, form.errors)
        if 'uid' not in post or 'code' not in post:
            return self.finish(RETCODE.FAILED)

        user = await User.check_reset_key(post['uid'], post['code'])
        if user:
            info = User.gen_password_and_salt(post['password'])
            user.password = info['password']
            user.salt = info['salt']
            user.reset_key = None
            user.save()
            user.refresh_key()
            self.setup_user_key(user.key, 30)
            self.finish(RETCODE.SUCCESS, {'id': user.id, 'nickname': user.nickname})
        else:
            self.finish(RETCODE.FAILED)

    @route.interface('POST')
    async def check_in(self):
        """ 签到 """
        if self.current_user:
            data = self.current_user.check_in()
            self.finish(RETCODE.SUCCESS, data)
        else:
            self.finish(RETCODE.FAILED)

    @route.interface('GET')
    async def get_userid(self):
        if self.current_user:
            self.finish(RETCODE.SUCCESS, {'id': to_hex(self.current_user.id)})
        else:
            self.finish(RETCODE.PERMISSION_DENIED)

    @route.interface('POST')
    @cooldown(config.USER_CHANGE_PASSWORD_COOLDOWN_BY_ACCOUNT, b'ic_cd_user_change_password_account_%b', unique_id_func=same_user)
    async def change_password(self):
        if self.current_user:
            post = await self.post_data()
            form = ChangePasswordForm(**post)
            if not form.validate():
                return self.finish(RETCODE.FAILED, form.errors)
            u: User = self.current_user
            if User.auth_by_mail(u.email, post['old_password']):
                u.set_password(post['password'])
                k = u.refresh_key()
                self.finish(RETCODE.SUCCESS, k['key'])
            else:
                self.finish(RETCODE.FAILED, {'old_password': ['旧密码不正确']})
        else:
            self.finish(RETCODE.PERMISSION_DENIED)

    @route.interface('POST')
    async def signout(self):
        if self.current_user:
            self.teardown_user_key()
            self.finish(RETCODE.SUCCESS)
        else:
            self.finish(RETCODE.FAILED)

    @route.interface('POST')
    @cooldown(config.USER_SIGNIN_COOLDOWN_BY_IP, b'ic_cd_user_signin_%b')
    @cooldown(config.USER_SIGNIN_COOLDOWN_BY_ACCOUNT, b'ic_cd_user_signin_account_%b', unique_id_func=same_email_post)
    async def signin(self):
        data = await self.post_data()

        form_email = SigninByEmailForm(**data)
        form_nickname = SigninByNicknameForm(**data)

        if form_email.validate():
            u = User.auth_by_mail(data['email'], data['password'])
        elif form_nickname.validate():
            u = User.auth_by_nickname(data['email'], data['password'])
        else:
            return self.finish(RETCODE.FAILED, form_email.errors)

        if u:
            expires = 30 if 'remember' in data else None
            u.refresh_key()
            self.setup_user_key(u.key, expires)
            self.finish(RETCODE.SUCCESS, {'id': u.id, 'access_token': u.key})
        else:
            self.finish(RETCODE.FAILED, '登录失败！')

    async def before_update(self, raw_post: Dict, values: SQLValuesToWrite, records: List[DataRecord]):
        if 'password' in raw_post:
            ret = User.gen_password_and_salt(raw_post['password'])
            values.update(ret)

        if 'key' in raw_post:
            values.update(User.gen_key())

    def after_update(self, raw_post: Dict, values: SQLValuesToWrite, old_records: List[DataRecord], records: List[DataRecord]):
        for old_record, record in zip(old_records, records):
            # 管理日志：重置访问令牌
            ManageLog.add_by_post_changed(self, 'key', MOP.USER_KEY_RESET, POST_TYPES.USER,
                                          values, old_record, record, value=None)

            # 管理日志：重置密码
            ManageLog.add_by_post_changed(self, 'password', MOP.USER_PASSWORD_CHANGE, POST_TYPES.USER,
                                          values, old_record, record, value=None)

    @cooldown(config.USER_SIGNUP_COOLDOWN_BY_IP, b'ic_cd_user_signup_%b', cd_if_unsuccessed=10)
    async def new(self):
        if config.EMAIL_ACTIVATION_ENABLE:
            return self.finish(RETCODE.FAILED, '此接口未开放')
        return await super().new()

    @route.interface('POST')
    @cooldown(config.USER_SIGNUP_COOLDOWN_BY_IP, b'ic_cd_user_signup_%b', cd_if_unsuccessed=10)
    async def request_signup_by_email(self):
        """
        提交邮件注册请求
        :return:
        """
        if not config.USER_ALLOW_SIGNUP:
            return self.finish(RETCODE.FAILED, '注册未开放')

        # 发送注册邮件
        if config.EMAIL_ACTIVATION_ENABLE:
            data = await self.post_data()

            form = RequestSignupByEmailForm(**data)
            if not form.validate():
                return self.finish(RETCODE.INVALID_POSTDATA, form.errors)

            email = form['email'].data.lower()
            code = await User.gen_reg_code_by_email(email, form['password'].data)
            await mail.send_reg_code_email(email, code)
            self.finish(RETCODE.SUCCESS)
        else:
            self.finish(RETCODE.FAILED, '此接口未开放')

    @route.interface('GET')
    async def check_reg_code_by_email(self):
        """ 检查与邮件关联的激活码是否可用 """
        pw = await User.check_reg_code_by_email(self.params['email'], self.params['code'])
        self.finish(RETCODE.SUCCESS if pw else RETCODE.FAILED)

    async def create_user(self, password, email=None, phone=None) -> User:
        values = {}
        nprefix = config.USER_NICKNAME_AUTO_PREFIX + '_'

        if config.POST_ID_GENERATOR != config.AutoGenerator:
            # 若不使用数据库生成id
            uid = User.gen_id()
            values['id'] = uid.to_bin()
            values['nickname'] = nprefix + uid.to_hex()

        values['change_nickname_chance'] = 1

        if email:
            values['email'] = email.lower()

        if phone:
            values['phone'] = phone

        # 密码
        ret = User.gen_password_and_salt(password)
        values.update(ret)

        values['group'] = USER_GROUP.NORMAL
        values['state'] = POST_STATE.NORMAL

        # 注册IP地址
        values['ip_registered'] = await get_fuzz_ip(self)

        # 生成 access_token
        values.update(User.gen_key())
        values['time'] = int(time.time())

        try:
            uid = User.insert(values).execute()
            u = User.get_by_pk(uid)
        except peewee.IntegrityError as e:
            db.rollback()
            if e.args[0].startswith('duplicate key'):
                return self.finish(RETCODE.ALREADY_EXISTS)
            return self.finish(RETCODE.FAILED)
        except peewee.DatabaseError:
            db.rollback()
            return self.finish(RETCODE.FAILED)

        times = 3
        success = False
        u.nickname = nprefix + to_hex(u.id.tobytes())

        # 尝试填充用户名
        while times >= 0:
            try:
                if u.number == 1:
                    u.group = USER_GROUP.ADMIN
                u.save()
                success = True
                break
            except peewee.DatabaseError:
                db.rollback()
                times -= 1
                u.nickname = nprefix + to_hex(os.urandom(8))

        if not success:
            return self.finish(RETCODE.FAILED)

        # 清理现场
        if email:
            await User.reg_code_cleanup(email)

        # 添加统计记录
        statistic_new(POST_TYPES.USER, u.id)
        UserNotifLastInfo.new(u.id)

        return u

    @route.interface('POST')
    async def signup_by_email(self):
        """ 确认并创建账户 """
        data = await self.post_data()

        if 'code' not in data or 'email' not in data:
            return self.finish(RETCODE.INVALID_POSTDATA)

        email = data['email'].lower()
        pw = await User.check_reg_code_by_email(email, data['code'])
        u = await self.create_user(pw, email=email)

        if pw and u:
            self.finish(RETCODE.SUCCESS, {'key': u.key, 'id': u.id})
        else:
            if self.is_finished: return
            self.finish(RETCODE.FAILED)

    @route.interface('POST')
    async def change_nickname(self):
        u = self.current_user
        if not u:
            return self.finish(RETCODE.PERMISSION_DENIED)

        post = await self.post_data()
        form = NicknameForm(**post)
        if not form.validate():
            return self.finish(RETCODE.INVALID_POSTDATA, form.errors)

        if u.change_nickname_chance > 0:
            try:
                old_nickname = u.nickname
                u.nickname = form['nickname'].data
                u.change_nickname_chance -= 1
                u.is_new_user = False
                u.save()
                self.finish(RETCODE.SUCCESS, {'nickname': u.nickname, 'change_nickname_chance': u.change_nickname_chance})
                ManageLog.add_by_post_changed(self, 'nickname', MOP.USER_NICKNAME_CHANGE, POST_TYPES.USER,
                                              True, {'nickname': old_nickname}, u, value=None)
                return
            except peewee.DatabaseError:
                db.rollback()

        self.finish(RETCODE.FAILED)
