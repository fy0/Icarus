import re
import time
import config
from typing import Dict, Type, List

from lib import mail
from model.log_manage import ManageLog, MANAGE_OPERATION as MOP
from model.notif import UserNotifLastInfo
from model._post import POST_TYPES, POST_STATE
from model.statistic import statistic_new
from slim.base.sqlquery import SQLValuesToWrite
from slim.base.user import BaseUser, BaseAccessTokenUserMixin
from slim.base.view import SQLQueryInfo
from slim.retcode import RETCODE
from slim.support.peewee import PeeweeView
from model.user import User, USER_GROUP
from slim.utils import to_hex, to_bin
from slim.utils.jsdict import JsDict
from view import route, ValidateForm, cooldown, same_user, get_fuzz_ip
from wtforms import StringField, validators as va, ValidationError
from slim.base.permission import Permissions, DataRecord
from view.permissions import permissions_add_all


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


class PasswordForm(ValidateForm):
    password = StringField('密码', validators=[
        va.required(),
        # va.Length(config.USER_PASSWORD_MIN, config.USER_PASSWORD_MAX)
    ])


class SigninForm(ValidateForm):
    email = StringField('邮箱', validators=[va.required(), va.Length(3, config.USER_EMAIL_MAX), va.Email()])

    password = StringField('密码', validators=[
        va.required(),
        # va.Length(config.USER_PASSWORD_MIN, config.USER_PASSWORD_MAX)
    ])


def nickname_check(form, field):
    # 至少两个汉字，或以汉字/英文字符开头至少4个字符
    text = '至少%d个汉字，或以汉字/英文字符开头至少%d个字符' % (config.USER_NICKNAME_CN_FOR_REG_MIN, config.USER_NICKNAME_FOR_REG_MIN)
    name = field.data
    # 检查首字符，检查有无非法字符
    if not re.match(r'^[\u4e00-\u9fa5a-zA-Z][\u4e00-\u9fa5a-zA-Z0-9]+$', name):
        raise ValidationError(text)
    # 若长度大于等于4，直接许可
    if len(name) >= max(config.USER_NICKNAME_FOR_REG_MIN, config.USER_NICKNAME_CN_FOR_REG_MIN):
        return True

    # 当最少汉字要求少于最少英文要求
    if config.USER_NICKNAME_CN_FOR_REG_MIN < config.USER_NICKNAME_FOR_REG_MIN:
        # 长度小于4，检查其中汉字数量
        if not (len(re.findall(r'[\u4e00-\u9fa5]', name)) >= config.USER_NICKNAME_CN_FOR_REG_MIN):
            raise ValidationError(text)
    elif config.USER_NICKNAME_CN_FOR_REG_MIN > config.USER_NICKNAME_FOR_REG_MIN:
        if not (len(re.findall(r'[a-zA-Z0-9]', name)) >= config.USER_NICKNAME_FOR_REG_MIN):
            raise ValidationError(text)

    if config.USER_NICKNAME_CHECK_FUNC and not config.USER_NICKNAME_CHECK_FUNC(name):
        raise ValidationError('昵称被保留')


class SignupForm(SigninForm):
    nickname = StringField('昵称', validators=[
        va.required(),
        va.Length(min(config.USER_NICKNAME_CN_FOR_REG_MIN, config.USER_NICKNAME_FOR_REG_MIN), config.USER_NICKNAME_FOR_REG_MAX),
        nickname_check
    ])

    password2 = StringField('重复密码', validators=[
        va.required(),
        va.EqualTo('password')
    ])


class ResetPasswordForm(ValidateForm):
    email = StringField('邮箱', validators=[va.required(), va.Length(3, config.USER_EMAIL_MAX), va.Email()])
    nickname = StringField('昵称', validators=[
        va.required(),
        va.Length(min(config.USER_NICKNAME_CN_FOR_REG_MIN, config.USER_NICKNAME_FOR_REG_MIN), config.USER_NICKNAME_FOR_REG_MAX),
        # nickname_check  # 发生了新旧可用昵称不同，然后找回密码出现了“昵称被占用”的情况
    ])


async def same_email_post(view):
    post = await view.post_data()
    if 'email' in post:
        return post['email'].encode('utf-8')


@route('user')
class UserView(UserMixin, PeeweeView):
    model = User

    @classmethod
    def permission_init(cls):
        permission: Permissions = cls.permission
        permissions_add_all(permission)

    @route.interface('POST')
    @cooldown(config.USER_REQUEST_PASSWORD_RESET_COOLDOWN_BY_ACCOUNT, b'ic_cd_user_request_reset_password_%b')
    @cooldown(config.USER_REQUEST_PASSWORD_RESET_COOLDOWN_BY_IP, b'ic_cd_user_request_reset_password_by_account_%b', unique_id_func=same_email_post)
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

    @route.interface('POST')
    async def resend_activation_mail(self):
        """ 重发激活邮件 """
        if config.EMAIL_ACTIVATION_ENABLE:
            if self.current_user:
                if await self.current_user.can_request_actcode():
                    await mail.send_register_activation(self.current_user)
                    self.finish(RETCODE.SUCCESS)
                else:
                    self.finish(RETCODE.TOO_FREQUENT)
            else:
                self.finish(RETCODE.PERMISSION_DENIED)
        else:
            self.finish(RETCODE.FAILED)

    @route.interface('GET')
    async def activation(self):
        """ 通过激活码激活 """
        user = await User.check_actcode(self.params['uid'], self.params['code'])
        if user:
            self.finish(RETCODE.SUCCESS, {'id': user.id, 'nickname': user.nickname})
        else:
            self.finish(RETCODE.FAILED)

    @route.interface('GET')
    async def get_userid(self):
        if self.current_user:
            self.finish(RETCODE.SUCCESS, {'id': to_hex(self.current_user.id)})
        else:
            self.finish(RETCODE.PERMISSION_DENIED)

    @route.interface('POST')
    @cooldown(config.USER_CHANGE_PASSWORD_COOLDOWN_BY_ACCOUNT, b'ic_cd_user_change_password_%b', unique_id_func=same_user)
    async def change_password(self):
        if self.current_user:
            post = await self.post_data()
            form = ChangePasswordForm(**post)
            if not form.validate():
                return self.finish(RETCODE.FAILED, form.errors)
            u: User = self.current_user
            if User.auth(u.email, post['old_password']):
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
    @cooldown(config.USER_SIGNIN_COOLDOWN_BY_ACCOUNT, b'ic_cd_user_signin_by_account_%b', unique_id_func=same_email_post)
    async def signin(self):
        data = await self.post_data()
        form = SigninForm(**data)
        if not form.validate():
            return self.finish(RETCODE.FAILED, form.errors)

        u = User.auth(data['email'], data['password'])
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
        return await super().new()

    async def before_insert(self, raw_post: Dict, values_lst: List[SQLValuesToWrite]):
        values = values_lst[0]
        # 必须存在以下值：
        # email password nickname
        # 自动填充或改写以下值：
        # id password salt group state key key_time time
        if not config.USER_ALLOW_SIGNUP:
            return self.finish(RETCODE.FAILED, '注册未开放')

        form = SignupForm(**raw_post)
        if not form.validate():
            return self.finish(RETCODE.FAILED, form.errors)

        if not config.POST_ID_GENERATOR == config.AutoGenerator:
            uid = User.gen_id().to_bin()
            values['id'] = uid

        values['email'] = values['email'].lower()

        ret = User.gen_password_and_salt(raw_post['password'])
        values.update(ret)

        if 'group' not in values:
            # 如果无权限，那此时即使带着 group 参数也被刷掉了，直接设为 normal
            if config.EMAIL_ACTIVATION_ENABLE:
                values['group'] = USER_GROUP.INACTIVE
            else:
                values['group'] = USER_GROUP.NORMAL

        if 'state' not in values:
            values['state'] = POST_STATE.NORMAL

        # 注册IP地址
        values['ip_registered'] = get_fuzz_ip(self)

        values.update(User.gen_key())
        values['time'] = int(time.time())
        self._key = values['key']

    async def after_insert(self, raw_post: Dict, values_lst: SQLValuesToWrite, records: List[DataRecord]):
        record = records[0]
        if record['number'] == 1:
            u = User.get(User.id == record['id'])
            u.group = USER_GROUP.ADMIN
            u.save()

        # 发送注册邮件
        if config.EMAIL_ACTIVATION_ENABLE:
            await mail.send_register_activation(record.val)

        # 添加统计记录
        statistic_new(POST_TYPES.USER, record['id'])
        UserNotifLastInfo.new(record['id'])

        record['access_token'] = self._key
