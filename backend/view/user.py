import os
import config
import hmac
from typing import Dict
from slim.support.peewee import PeeweeView
from model.user import User, USER_GROUP, USER_STATE
from slim.utils import ObjectID
from view import route


@route('user')
class UserView(PeeweeView):
    model = User

    def handle_query(self, values: Dict):
        if 'password' in values:
            values.update(User.gen_password_and_salt(values['password']))
        return values

    def handle_insert(self, values: Dict):
        # 必须存在以下值：
        # username nickname password [email]
        # 自动填充或改写以下值：
        # id password salt group state key key_time reg_time

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

        return values
