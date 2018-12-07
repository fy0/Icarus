from slim.base.sqlquery import SQLQueryInfo, SQL_OP
from slim.base.permission import Ability
from model._post import POST_VISIBLE, POST_STATE
from permissions.roles import *

base_post_state_conditions = [
    ('state', '>', POST_STATE.APPLY),
]


def ignore_post_invisible(ability: Ability, user, query: 'SQLQueryInfo'):
    roles = {ability.role} if not user else set(user.roles)
    if roles & {'superuser', 'admin'}:
        return

    if roles & {'inactive_user', 'user', 'wiki_editor'}:
        visible_limit = POST_VISIBLE.ADMIN_ONLY
    else:
        visible_limit = POST_VISIBLE.USER_ONLY

    query.add_condition('visible', '>', POST_VISIBLE.HIDE)
    query.add_condition('visible', '<', visible_limit)


def post_visible_work(table):
    # state 约束
    visitor.add_query_condition(table, base_post_state_conditions)
    banned_user.add_query_condition(table, base_post_state_conditions)
    inactive_user.add_query_condition(table, base_post_state_conditions)
    normal_user.add_query_condition(table, base_post_state_conditions)

    # visible 约束（动态），还是这四个的原因是
    # 做请求的时候并不会以高权限身份来做，记住真实role和请求role是不同的
    visitor.add_query_condition(table, func=ignore_post_invisible)
    banned_user.add_query_condition(table, func=ignore_post_invisible)
    inactive_user.add_query_condition(table, func=ignore_post_invisible)
    normal_user.add_query_condition(table, func=ignore_post_invisible)
