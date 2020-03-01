import json
import os
import time
import peewee
import config
from typing import Dict, List, Type, Union
from lib import mail
from model import db
from model.manage_log import ManageLog, MANAGE_OPERATION as MOP
from model.notif import UserNotifLastInfo
from model._post import POST_TYPES, POST_STATE
from model.post_stats import post_stats_new
from slim.base.sqlquery import SQLValuesToWrite
from slim.base.user import BaseAccessTokenUserViewMixin, BaseUser, BaseUserViewMixin
from slim.base.view import BaseView
from slim.retcode import RETCODE
from model.user import User, USER_GROUP
from slim.utils import to_hex, to_bin, get_bytes_from_blob
from api import route, ValidateForm, cooldown, same_user, get_fuzz_ip
from wtforms import StringField, validators as va
from slim.base.permission import DataRecord
from api.user_signup_legacy import UserLegacyView
from api.user_validate_form import RequestSignupByEmailForm, SigninByEmailForm, SigninByNicknameForm, PasswordForm, \
    NicknameForm
from api.validate.user import ValidatePasswordResetPost, ChangePasswordDataModel


class UserViewMixin(BaseAccessTokenUserViewMixin):
    def get_user_by_token(self: Union['BaseUserViewMixin', 'BaseView'], token) -> Type[BaseUser]:
        try: return User.get_by_key(to_bin(token))
        except: pass

    def setup_user_token(self: Union['BaseUserViewMixin', 'BaseView'], user_id, key=None, expires=30):
        pass

    def teardown_user_token(self: Union['BaseUserViewMixin', 'BaseView'], token=None):
        u: User = self.current_user
        u.key = None
        u.save()


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
class UserView(UserViewMixin, UserLegacyView):
    model = User

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

    @route.interface('GET', summary='测试专用1', va_query=ValidatePasswordResetPost)
    async def test1(self):
        pass

    @route.interface('POST', summary='测试专用2', va_query=ValidatePasswordResetPost, va_post=ValidatePasswordResetPost)
    async def test2(self):
        pass

    @route.interface('POST', summary='密码重置验证', va_post=ValidatePasswordResetPost)
    async def validate_password_reset(self):
        """
        忘记密码后，进入重设流程时，通过此接口提交校验码和新密码
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

    @route.interface('POST', va_post=ChangePasswordDataModel)
    @cooldown(config.USER_CHANGE_PASSWORD_COOLDOWN_BY_ACCOUNT, b'ic_cd_user_change_password_account_%b', unique_id_func=same_user)
    async def change_password(self):
        if self.current_user:
            vpost: ChangePasswordDataModel = self._.validated_post

            u: User = self.current_user
            if User.auth_by_mail(u.email, vpost.old_password):
                u.set_password(vpost.password)
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
            self.setup_user_token(u.id, u.key, expires)
            self.finish(RETCODE.SUCCESS, {'id': u.id, 'access_token': u.key})
        else:
            self.finish(RETCODE.FAILED, '登录失败！')

    async def get(self):
        await super().get()
        uid = self.params.get('id', None)
        # 满足条件：请求参数有用户，当前用户已登录，请求查询的是当前用户
        if uid and self.current_user and (uid == self.current_user.id.hex()):
            if self.ret_val['code'] == RETCODE.SUCCESS:
                data = self.ret_val['data']
                data['roles'] = self.roles
                data['main_role'] = self.current_user.main_role
                self.finish(RETCODE.SUCCESS, data)

    async def update(self):
        post = await self.post_data()
        if 'password' in post:
            # 直接的密码重置过不了校验，所以hack一下
            self.new_pass = post['password']
            post['password'] = '00'
        await super().set()

    async def before_update(self, values: SQLValuesToWrite, records: List[DataRecord]):
        raw_post = await self.post_data()

        if 'password' in raw_post:
            ret = User.gen_password_and_salt(self.new_pass)
            values.update(ret)

        if 'key' in raw_post:
            values.update(User.gen_key())

    async def after_update(self, values: SQLValuesToWrite, old_records: List[DataRecord],
                           new_records: List[DataRecord]):
        raw_post = await self.post_data()
        for old_record, record in zip(old_records, new_records):
            manage_try_add = lambda column, op: ManageLog.add_by_post_changed(
                self, column, op, POST_TYPES.USER, values, old_record, record
            )

            # 管理日志：重置访问令牌
            ManageLog.add_by_post_changed(self, 'key', MOP.USER_KEY_RESET, POST_TYPES.USER,
                                          values, old_record, record, value=None)

            # 管理日志：重置密码
            ManageLog.add_by_post_changed(self, 'password', MOP.USER_PASSWORD_CHANGE, POST_TYPES.USER,
                                          values, old_record, record, value=None)

            manage_try_add('state', MOP.POST_STATE_CHANGE)
            manage_try_add('visible', MOP.POST_VISIBLE_CHANGE)

            manage_try_add('group', MOP.USER_GROUP_CHANGE)
            manage_try_add('exp', MOP.USER_EXP_CHANGE)

            def manage_try_add_resource(column, op):
                if column not in values: return
                uid = self.current_user.id
                src = json.loads(raw_post['$src'])
                # TODO: 检查一下是否真的存在

                def func(info):
                    info['related_type'] = src['type']
                    info['related_id'] = to_bin(src['id'])
                    info['related_user_id'] = uid

                ManageLog.add_by_post_changed(self, column, op, POST_TYPES.USER, values, old_record, record, cb=func)

            manage_try_add_resource('credit', MOP.USER_CREDIT_CHANGE)
            manage_try_add_resource('repute', MOP.USER_REPUTE_CHANGE)

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

        values['is_new_user'] = True
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
        u.nickname = nprefix + to_hex(get_bytes_from_blob(u.id))

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
        post_stats_new(POST_TYPES.USER, u.id)
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
        if not pw:
            return self.finish(RETCODE.FAILED)

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
                # note: 虽然有点奇怪，但下面这句其实没问题 18.11.13
                ManageLog.add_by_post_changed(self, 'nickname', MOP.USER_NICKNAME_CHANGE, POST_TYPES.USER,
                                              True, {'nickname': old_nickname}, u)
                return
            except peewee.DatabaseError:
                db.rollback()

        self.finish(RETCODE.FAILED)
