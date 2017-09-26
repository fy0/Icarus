from typing import Dict

import config
from slim.retcode import RETCODE
from slim.support.peewee import PeeweeView
from model.user import User, USER_GROUP, USER_STATE
from view import route


@route('user')
class UserView(PeeweeView):
    model = User

    @staticmethod
    def handle_query(values: Dict):
        if 'password' in values:
            values.update(User.gen_password_and_salt(values['password']))

    @staticmethod
    def handle_insert(values: Dict):
        # 必须存在以下值：
        # username nickname password [email]
        # 自动填充或改写以下值：
        # id password salt group state key key_time reg_time

        if not config.USER_ALLOW_SIGNUP:
            return RETCODE.FAILED, '注册未开放'

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
