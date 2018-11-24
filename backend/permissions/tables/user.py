from model.user import USER_GROUP
from permissions.roles import *
from model._post import POST_STATE, POST_VISIBLE
from slim.base.permission import Ability, A, DataRecord
from slim.base.sqlquery import SQLQueryInfo, SQL_OP


# 如果查询的是自己，附带部分信息
def func(ability: Ability, user, query: 'SQLQueryInfo'):
    for i in query.conditions.find('id'):
        if i[1] == SQL_OP.EQ and i[2] == user.id.hex():
            query.select.add('email')
            query.select.add('phone')
            query.select.add('key_time')
            query.select.add('access_time')
            query.select.add('is_new_user')
            query.select.add('phone_verified')
            query.select.add('change_nickname_chance')


banned_user.add_query_condition('user', func=func)
inactive_user.add_query_condition('user', func=func)
normal_user.add_query_condition('user', func=func)


def check_is_me(ability, user, action, record: DataRecord, available_columns: list):
    # 拒绝其他人写入自己的个人资料
    if user:
        if record.get('id') != user.id:
            available_columns.clear()
    return True


def check_is_admin(ability, user, action, record: DataRecord, available_columns: list):
    # 阻止superuser写入superuser或更高权限用户组
    if user:
        if record.get('group') in (USER_GROUP.SUPERUSER, USER_GROUP.ADMIN):
            # 只允许写这两列
            available_columns[:] = filter(lambda x: x in {'credit', 'repute'}, available_columns)
    return True


banned_user.add_record_check((A.WRITE,), 'user', func=check_is_me)
inactive_user.add_record_check((A.WRITE,), 'user', func=check_is_me)
normal_user.add_record_check((A.WRITE,), 'user', func=check_is_me)

superuser.add_record_check((A.WRITE,), 'user', func=check_is_admin)
