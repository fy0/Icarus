import os
import re
import time
import config
from typing import Dict, List
from model.notif import UserNotifLastInfo
from model._post import POST_TYPES, POST_STATE
from model.post_stats import post_stats_new
from slim.base.sqlquery import SQLValuesToWrite
from slim.retcode import RETCODE
from slim.support.peewee import PeeweeView
from model.user import User, USER_GROUP
from view import route, ValidateForm, cooldown, same_user, get_fuzz_ip
from wtforms import StringField, validators as va, ValidationError
from slim.base.permission import Permissions, DataRecord
from view.user_validate_form import nickname_check


class SignupFormLegacy(ValidateForm):
    email = StringField('邮箱', validators=[va.required(), va.Length(3, config.USER_EMAIL_MAX), va.Email()])

    password = StringField('密码', validators=[
        va.required(),
        # va.Length(config.USER_PASSWORD_MIN, config.USER_PASSWORD_MAX)
    ])

    nickname = StringField('昵称', validators=[
        va.required(),
        va.Length(min(config.USER_NICKNAME_CN_FOR_REG_MIN, config.USER_NICKNAME_FOR_REG_MIN), config.USER_NICKNAME_FOR_REG_MAX),
        nickname_check
    ])

    password2 = StringField('重复密码', validators=[
        va.required(),
        va.EqualTo('password')
    ])


class UserLegacyView(PeeweeView):
    model = User

    @cooldown(config.USER_SIGNUP_COOLDOWN_BY_IP, b'ic_cd_user_signup_%b', cd_if_unsuccessed=10)
    async def new(self):
        if config.EMAIL_ACTIVATION_ENABLE:
            return self.finish(RETCODE.FAILED, '此接口未开放')
        return await super().new()

    async def before_insert(self, raw_post: Dict, values_lst: List[SQLValuesToWrite]):
        values = values_lst[0]
        # 必须存在以下值：
        # email password nickname
        # 自动填充或改写以下值：
        # id password salt group state key key_time time
        if not config.USER_ALLOW_SIGNUP:
            return self.finish(RETCODE.FAILED, '注册未开放')

        form = SignupFormLegacy(**raw_post)
        if not form.validate():
            return self.finish(RETCODE.FAILED, form.errors)

        if not config.POST_ID_GENERATOR == config.AutoGenerator:
            uid = User.gen_id().to_bin()
            values['id'] = uid

        values['email'] = values['email'].lower()

        ret = User.gen_password_and_salt(raw_post['password'])
        values.update(ret)

        if 'group' not in values:
            # 如果无权限，那此时即使带着 group 参数也被刷掉了，直接设为 normal 即可
            values['group'] = USER_GROUP.NORMAL

        if 'state' not in values:
            values['state'] = POST_STATE.NORMAL

        # 注册IP地址
        values['ip_registered'] = await get_fuzz_ip(self)

        values.update(User.gen_key())
        values['time'] = int(time.time())
        self._key = values['key']

    async def after_insert(self, raw_post: Dict, values_lst: SQLValuesToWrite, records: List[DataRecord]):
        record = records[0]
        if record['number'] == 1:
            u = User.get(User.id == record['id'])
            u.group = USER_GROUP.ADMIN
            u.save()

        # 添加统计记录
        post_stats_new(POST_TYPES.USER, record['id'])
        UserNotifLastInfo.new(record['id'])

        record['access_token'] = self._key
