import re
import config
from typing import Dict
from slim.retcode import RETCODE
from slim.support.peewee import PeeweeView
from model.user import User, USER_GROUP, USER_STATE
from view import route, ValidateForm
from wtforms import StringField, validators as va


class SignupForm(ValidateForm):
    username = StringField('用户名', validators=[
        va.required(),
        va.Length(config.USERNAME_FOR_REG_MIN, config.USERNAME_FOR_REG_MAX),
        va.Regexp('^[a-zA-Z][a-zA-Z0-9]+$', message='用户名应为英文与数字的组合，同时首字为英文')
    ])

    password = StringField('密码', validators=[
        va.required(),
        va.Length(config.PASSWORD_MIN, config.PASSWORD_MAX)
    ])

    password2 = StringField('重复密码', validators=[
        va.required(),
        va.EqualTo('password')
    ])

    email = StringField('邮箱', validators=[va.required(), va.Email()])


@route('user')
class UserView(PeeweeView):
    model = User

    @classmethod
    def handle_query(cls, values: Dict):
        if 'password' in values:
            values.update(User.gen_password_and_salt(values['password']))

    @classmethod
    def handle_insert(cls, values: Dict):
        # 必须存在以下值：
        # username password [email]
        # 自动填充或改写以下值：
        # id password salt group state key key_time reg_time

        if not config.USER_ALLOW_SIGNUP:
            return RETCODE.FAILED, '注册未开放'

        form = SignupForm(**values)
        if not form.validate():
            return RETCODE.FAILED, form.errors

        uid = User.gen_id()
        values['id'] = uid.digest()

        ret = User.gen_password_and_salt(values['password'])
        values.update(ret)

        if 'group' not in values:
            # 如果无权限，那此时即使带着 group 参数也被刷掉了，直接设为 normal
            values['group'] = USER_GROUP.NORMAL

        if 'state' not in values:
            values['state'] = USER_STATE.NORMAL

        values.update(User.gen_key())
        values['reg_time'] = uid.time
