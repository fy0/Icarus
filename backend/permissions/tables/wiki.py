from model.board import Board
from permissions.roles import *
from model._post import POST_STATE, POST_VISIBLE
from permissions.tables._vars import post_visible_work
from slim.base.permission import Ability, A, DataRecord
from slim.base.sqlquery import SQLQueryInfo, SQL_OP


post_visible_work('wiki_article')


# 非登录不能查看内容的正文
def check_remove_content_for_select(ability, user, action, record: DataRecord, available_columns: list):
    if user:
        if record.get('visible') == POST_VISIBLE.CONTENT_IF_LOGIN:
            available_columns.remove('content')
    return True


visitor.add_record_check((A.READ,), 'wiki_article', func=check_remove_content_for_select)
banned_user.add_record_check((A.READ,), 'wiki_article', func=check_remove_content_for_select)
inactive_user.add_record_check((A.READ,), 'wiki_article', func=check_remove_content_for_select)
normal_user.add_record_check((A.READ,), 'wiki_article', func=check_remove_content_for_select)


# 不准其他用户写入当前用户的文章
def check_is_users_post(ability, user, action, record: DataRecord, available_columns: list):
    if user:
        if record.get('user_id') != user.id:
            available_columns.clear()
    return True


normal_user.add_record_check((A.WRITE,), 'wiki_article', func=check_is_users_post)
