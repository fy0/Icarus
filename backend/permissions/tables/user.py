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
            query.select.add('is_new_user')
            query.select.add('phone_verified')
            query.select.add('change_nickname_chance')


banned_user.add_query_condition('user', func=func)
inactive_user.add_query_condition('user', func=func)
normal_user.add_query_condition('user', func=func)


# 拒绝其他人写入自己的个人资料

def check_is_user(ability, user, action, record: DataRecord, available_columns: list):
    if user:
        if record.get('id') != user.id:
            available_columns.clear()
    return True


banned_user.add_record_check((A.WRITE,), 'user', func=check_is_user)
inactive_user.add_record_check((A.WRITE,), 'user', func=check_is_user)
normal_user.add_record_check((A.WRITE,), 'user', func=check_is_user)
