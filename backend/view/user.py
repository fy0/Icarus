import re
import config
from typing import Dict

from slim.base.permission import Permissions, Ability, BaseUser, AbilityRecord, AbilityColumn
from slim.base.view import ParamsQueryInfo
from slim.retcode import RETCODE
from slim.support.peewee import PeeweeView
from model.user import User, USER_GROUP, USER_STATE
from slim.utils import to_hex, to_bin
from view import route, ValidateForm
from wtforms import StringField, validators as va


class SigninForm(ValidateForm):
    email = StringField('邮箱', validators=[va.required(), va.Email()])

    password = StringField('密码', validators=[
        va.required(),
        va.Length(config.PASSWORD_MIN, config.PASSWORD_MAX)
    ])


class SignupForm(SigninForm):
    password2 = StringField('重复密码', validators=[
        va.required(),
        va.EqualTo('password')
    ])


@route('user')
class UserView(PeeweeView):
    model = User

    @classmethod
    def interface(cls):
        super().interface()
        cls.use('signin', 'POST')

    def get_current_user(self):
        key = self.get_secure_cookie('u')
        return User.get_by_key(to_bin(key))

    @classmethod
    def permission_init(cls):
        cls.permission: Permissions
        visitor = Ability(None, {
            'user': {
                'id': ['query', 'read'],
                'group': ['read'],

                'email': ['create'],
                'password': ['create'],
            }
        })

        def func(ability, user, cur_action, record: AbilityRecord) -> bool:
            return False
            #return True

        visitor.add_record_rule(
            ['query', 'read', 'write'],
            AbilityColumn('user', 'key'),
            func=func
        )

        test = Ability('test', {
            'user': {
                'nickname': ['query', 'read', 'write'],
                'key': ['query', 'read']
            }
        }, based_on=visitor)

        admin = Ability('admin', {
            'user': '*'
        })

        cls.permission.add(visitor)
        cls.permission.add(test)
        cls.permission.add(admin)

    async def signin(self):
        data = await self.post_data()
        form = SigninForm(**data)
        if not form.validate():
            return RETCODE.FAILED, form.errors

        u = User.auth(data['email'], data['password'])
        if u:
            expires = 30 if 'remember' in data else None
            self.set_secure_cookie('u', u.key.hex(), max_age=expires)
            self.finish(RETCODE.SUCCESS, '登录成功')
        else:
            self.finish(RETCODE.FAILED, '登录失败！')

    @classmethod
    def handle_insert(cls, values: Dict):
        # 必须存在以下值：
        # email password
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
