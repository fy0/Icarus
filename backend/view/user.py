import re
import config
from typing import Dict, Type

from model.post import POST_TYPES
from model.statistic import statistic_new
from slim.base.user import BaseUser, BaseAccessTokenUserMixin
from slim.base.view import ParamsQueryInfo
from slim.retcode import RETCODE
from slim.support.peewee import PeeweeView
from model.user import User, USER_GROUP, USER_STATE
from slim.utils import to_hex, to_bin
from view import route, ValidateForm
from wtforms import StringField, validators as va, ValidationError
from slim.base.permission import Permissions, Ability, AbilityRecord, AbilityColumn, A


class UserMixin(BaseAccessTokenUserMixin):
    def teardown_user_key(self):
        u: User = self.current_user
        u.update(key=None).execute()

    def get_user_by_key(self, key):
        if not key: return
        try:
            return User.get_by_key(to_bin(key))
        except:
            pass


class SigninForm(ValidateForm):
    email = StringField('邮箱', validators=[va.required(), va.Length(3, config.EMAIL_MAX), va.Email()])

    password = StringField('密码', validators=[
        va.required(),
        va.Length(config.PASSWORD_MIN, config.PASSWORD_MAX)
    ])


def nickname_check(form, field):
    # 至少两个汉字，或以汉字/英文字符开头至少4个字符
    text = '至少%d个汉字，或以汉字/英文字符开头至少%d个字符' % (config.NICKNAME_CN_FOR_REG_MIN, config.NICKNAME_FOR_REG_MIN)
    name = field.data
    # 检查首字符，检查有无非法字符
    if not re.match(r'^[\u4e00-\u9fa5a-zA-Z][\u4e00-\u9fa5a-zA-Z0-9]+$', name):
        raise ValidationError(text)
    # 若长度大于等于4，直接许可
    if len(name) >= max(config.NICKNAME_FOR_REG_MIN, config.NICKNAME_CN_FOR_REG_MIN):
        return True

    # 当最少汉字要求少于最少英文要求
    if config.NICKNAME_CN_FOR_REG_MIN < config.NICKNAME_FOR_REG_MIN:
        # 长度小于4，检查其中汉字数量
        if not (len(re.findall(r'[\u4e00-\u9fa5]', name)) >= config.NICKNAME_CN_FOR_REG_MIN):
            raise ValidationError(text)
    elif config.NICKNAME_CN_FOR_REG_MIN > config.NICKNAME_FOR_REG_MIN:
        if not (len(re.findall(r'[a-zA-Z0-9]', name)) >= config.NICKNAME_FOR_REG_MIN):
            raise ValidationError(text)


class SignupForm(SigninForm):
    nickname = StringField('昵称', validators=[
        va.required(),
        va.Length(min(config.NICKNAME_CN_FOR_REG_MIN, config.NICKNAME_FOR_REG_MIN), config.NICKNAME_FOR_REG_MAX),
        nickname_check
    ])

    password2 = StringField('重复密码', validators=[
        va.required(),
        va.EqualTo('password')
    ])


@route('user')
class UserView(UserMixin, PeeweeView):
    model = User

    @classmethod
    def permission_init(cls):
        permission: Permissions = cls.permission
        visitor = Ability(None, {
            'user': {
                'id': [A.QUERY, A.READ],
                'nickname': [A.READ, A.CREATE],
                'group': [A.READ],

                'email': [A.CREATE],
                'password': [A.CREATE],
            }
        })

        normal_user = Ability('user', {
            'user': {
                'nickname': [A.QUERY, A.READ, A.WRITE],

                # 'key': ['query', 'read']
            }
        }, based_on=visitor)

        def user_check(ability, user, action, record: AbilityRecord, available_columns: list):
            if user and record.get('id') == user.id:
                available_columns.append('email')
            return True

        normal_user.add_record_check([A.READ], 'user', func=user_check)

        admin = Ability('admin', {
            'user': '*'
        })

        permission.add(visitor)
        permission.add(normal_user)
        permission.add(admin)

    @route.interface('GET')
    async def get_userid(self):
        if self.current_user:
            self.finish(RETCODE.SUCCESS, {'id': to_hex(self.current_user.id)})
        else:
            self.finish(RETCODE.PERMISSION_DENIED)

    @route.interface('POST')
    async def signout(self):
        self.teardown_user_key()
        self.finish(RETCODE.SUCCESS)

    @route.interface('POST')
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

    def before_insert(self, raw_post: Dict, values: Dict):
        # 必须存在以下值：
        # email password nickname
        # 自动填充或改写以下值：
        # id password salt group state key key_time reg_time
        if not config.USER_ALLOW_SIGNUP:
            return RETCODE.FAILED, '注册未开放'

        form = SignupForm(**raw_post)
        if not form.validate():
            return RETCODE.FAILED, form.errors

        uid = User.gen_id()
        values['id'] = uid.digest()
        values['email'] = values['email'].lower()

        ret = User.gen_password_and_salt(values['password'])
        values.update(ret)

        if 'group' not in values:
            # 如果无权限，那此时即使带着 group 参数也被刷掉了，直接设为 normal
            values['group'] = USER_GROUP.NORMAL

        if 'state' not in values:
            values['state'] = USER_STATE.NORMAL

        values.update(User.gen_key())
        values['reg_time'] = uid.time
        self._key = values['key']

        # 添加统计记录
        statistic_new(POST_TYPES.USER, values['id'])

    def after_insert(self, values: Dict):
        values['access_token'] = self._key
