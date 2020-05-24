import binascii
import json
import os
import time
import peewee
import config
from typing import Dict, List, Type, Union

from app import app
from lib import mail
from model import db
from model.manage_log import ManageLog, MANAGE_OPERATION as MOP
from model.notif import UserNotifLastInfo
from model._post import POST_TYPES, POST_STATE
from model.post_stats import post_stats_new
from model.user_token import UserToken
from slim import D
from slim.base.sqlquery import SQLValuesToWrite
from slim.base.user import BaseAccessTokenUserViewMixin, BaseUser, BaseUserViewMixin
from slim.base.view import BaseView
from slim.retcode import RETCODE
from model.user import User, USER_GROUP
from slim.support.peewee import PeeweeView
from slim.utils import to_hex, to_bin, get_bytes_from_blob, sentinel
from api import ValidateForm, cooldown, same_user, get_fuzz_ip, run_in_thread
from slim.base.permission import DataRecord
from api.validate.user import ValidatePasswordResetPostDataModel, ChangePasswordDataModel, SignupDirectDataModel, \
    SignupConfirmByEmailDataModel, SignupRequestByEmailDataModel, SigninDataModel, ChangeNicknameDataModel, \
    RequestResetPasswordDataModel
from api.user_view_mixin import UserViewMixin


async def same_email_post(view):
    post = await view.post_data()
    if 'email' in post:
        return post['email'].lower().encode('utf-8')


@app.route.view('user')
class UserView(UserViewMixin, PeeweeView):
    model = User

    @app.route.interface('POST', va_post=RequestResetPasswordDataModel)
    @cooldown(config.USER_REQUEST_PASSWORD_RESET_COOLDOWN_BY_IP, b'ic_cd_user_request_reset_password_%b')
    @cooldown(config.USER_REQUEST_PASSWORD_RESET_COOLDOWN_BY_ACCOUNT, b'ic_cd_user_request_reset_password_account_%b', unique_id_func=same_email_post)
    async def request_password_reset(self):
        """
        申请重置密码 / 忘记密码
        :return:
        """
        vpost: RequestResetPasswordDataModel = self._.validated_post

        try:
            user: User = User.get(User.nickname == vpost.nickname, User.email == vpost.email)
        except User.DoesNotExist:
            user = None

        if user:
            if await user.can_request_reset_password():
                key = user.gen_reset_key()
                user.reset_key = key
                user.save()
                await mail.send_password_reset(user)
                return self.finish(RETCODE.SUCCESS, {'id': user.id, 'nickname': user.nickname})

        self.finish(RETCODE.FAILED)

    @app.route.interface('POST', summary='密码重置验证', va_post=ValidatePasswordResetPostDataModel)
    async def validate_password_reset(self):
        """
        忘记密码后，进入重设流程时，通过此接口提交校验码和新密码
        :return:
        """
        vpost: ValidatePasswordResetPostDataModel = self._.validated_post

        user = await User.check_reset_key(vpost.uid, vpost.code)
        if user:
            info = User.gen_password_and_salt(vpost.password)
            user.password = info['password']
            user.salt = info['salt']
            user.reset_key = None
            user.save()

            UserToken.clear_by_user_id(user.id)
            t: UserToken = await self.setup_user_token(user.id)
            self.finish(RETCODE.SUCCESS, {'id': user.id, 'nickname': user.nickname, 'access_token': t.get_token()})
        else:
            self.finish(RETCODE.FAILED)

    @app.route.interface('POST')
    async def check_in(self):
        """ 签到 """
        if self.current_user:
            data = self.current_user.check_in()
            self.finish(RETCODE.SUCCESS, data)
        else:
            self.finish(RETCODE.FAILED)

    @app.route.interface('POST', va_post=ChangePasswordDataModel)
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

    @app.route.interface('POST', summary='登出')
    async def signout(self):
        if self.current_user:
            self.teardown_user_token(self.current_user)
            self.finish(RETCODE.SUCCESS)
        else:
            self.finish(RETCODE.FAILED)

    @app.route.interface('POST', va_post=SigninDataModel)
    @cooldown(config.USER_SIGNIN_COOLDOWN_BY_IP, b'ic_cd_user_signin_%b')
    @cooldown(config.USER_SIGNIN_COOLDOWN_BY_ACCOUNT, b'ic_cd_user_signin_account_%b', unique_id_func=same_email_post)
    async def signin(self):
        vpost: SigninDataModel = self._.validated_post

        # check auth method
        if vpost.email:
            field_value = vpost.email
            auth_method = User.auth_by_mail
        elif vpost.username:
            field_value = vpost.username
            auth_method = User.auth_by_username
        else:
            return self.finish(RETCODE.FAILED, msg='必须提交用户名或邮箱中的一个作为登录凭据')

        # auth and generate access token
        user, success = await run_in_thread(auth_method, field_value, vpost.password)

        if user:
            # expires = 30 if 'remember' in data else None
            t: UserToken = await self.setup_user_token(user.id)
            self.finish(RETCODE.SUCCESS, {'id': user.id, 'access_token': t.get_token()})
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
        return self.finish(RETCODE.FAILED)
        if config.EMAIL_ACTIVATION_ENABLE:
            return self.finish(RETCODE.FAILED, '此接口未开放')
        return await super().new()

    @app.route.interface('POST', va_post=SignupRequestByEmailDataModel, summary='注册申请（邮箱）')
    @cooldown(config.USER_SIGNUP_COOLDOWN_BY_IP, b'ic_cd_user_signup_%b', cd_if_unsuccessed=10)
    async def signup_request_by_email(self):
        """
        提交邮件注册请求
        :return:
        """
        if not config.USER_ALLOW_SIGNUP:
            return self.finish(RETCODE.FAILED, '注册未开放')

        # 发送注册邮件
        if config.EMAIL_ACTIVATION_ENABLE:
            vpost: SignupRequestByEmailDataModel = self._.validated_post
            code = await User.gen_reg_code_by_email(vpost.email, vpost.password)
            await mail.send_reg_code_email(vpost.email, code)
            self.finish(RETCODE.SUCCESS)
        else:
            self.finish(RETCODE.FAILED, '此接口未开放')

    @app.route.interface('GET', va_query=SignupConfirmByEmailDataModel, summary='检查注册码和邮箱是否匹配')
    async def check_reg_code_by_email(self):
        """ 检查与邮件关联的激活码是否可用 """
        vquery: SignupConfirmByEmailDataModel = self._.validated_query
        pw = await User.check_reg_code_by_email(vquery.email, vquery.code)
        self.finish(RETCODE.SUCCESS if pw else RETCODE.FAILED)

    @app.route.interface('POST', va_post=SignupConfirmByEmailDataModel, summary='注册确认（邮箱）')
    async def signup_confirm_by_email(self):
        """ 确认并创建账户 """
        vpost: SignupConfirmByEmailDataModel = self._.validated_post

        password = await User.check_reg_code_by_email(vpost.email, vpost.code)
        if not password:
            return self.finish(RETCODE.FAILED, '验证码不正确')

        u = User.new(None, password, {'email': vpost.email}, auto_nickname=True)
        await self.signup_cleanup(u)

    @app.route.interface('POST', va_post=SignupDirectDataModel, summary='注册（直接形式）')
    async def signup_by_direct(self):
        if self.current_user:
            return self.finish(RETCODE.PERMISSION_DENIED)  # 已登录用户凑什么热闹

        vpost: SignupDirectDataModel = self._.validated_post
        extra_values = {
            'email': vpost.email,
            'ip_registered': await get_fuzz_ip(self)
        }

        u = User.new(vpost.nickname, vpost.password, extra_values=extra_values, is_for_tests=False, auto_nickname=False)
        await self.signup_cleanup(u)

    async def signup_cleanup(self, u):
        if u:
            # 添加统计记录
            post_stats_new(POST_TYPES.USER, u.id)
            UserNotifLastInfo.new(u.id)

            if u.email:
                await User.reg_code_cleanup(u.email)

            t: UserToken = await self.setup_user_token(u.id)
            self.finish(RETCODE.SUCCESS, {'id': u.id, 'access_token': t.get_token()})
        else:
            self.finish(RETCODE.FAILED)

    @app.route.interface('POST', va_post=ChangeNicknameDataModel, summary='使用改名卡修改昵称')
    async def change_nickname(self):
        u: User = self.current_user
        if not u:
            return self.finish(RETCODE.PERMISSION_DENIED)

        vpost: ChangeNicknameDataModel = self._.validated_post

        if u.change_nickname_chance > 0:
            try:
                old_nickname = u.nickname
                u.nickname = vpost.nickname
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
