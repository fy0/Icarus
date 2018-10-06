from permissions.roles import *
from model._post import POST_STATE, POST_VISIBLE
from slim.base.permission import Ability, A, DataRecord
from slim.base.sqlquery import SQLQueryInfo, SQL_OP


# 限定用户只能查询自己的上传
def func(ability, user, query: 'SQLQueryInfo'):
    query.add_condition('user_id', '==', user.id)


banned_user.add_query_condition('upload', func=func)
inactive_user.add_query_condition('upload', func=func)
normal_user.add_query_condition('upload', func=func)
