from model.board import Board
from permissions.roles import *
from model._post import POST_STATE, POST_VISIBLE
from permissions.tables._vars import post_visible_work
from slim.base.permission import Ability, A, DataRecord
from slim.base.sqlquery import SQLQueryInfo, SQL_OP


post_visible_work('topic')


# 非登录不能查看内容的正文
def check_remove_content_for_select(ability, user, action, record: DataRecord, available_columns: list):
    if record.get('visible') == POST_VISIBLE.CONTENT_IF_LOGIN:
        if not user:
            available_columns.remove('content')
    elif record.get('visible') == POST_VISIBLE.ADMIN_ONLY:
        pass
    return True


visitor.add_record_check((A.READ,), 'topic', func=check_remove_content_for_select)
banned_user.add_record_check((A.READ,), 'topic', func=check_remove_content_for_select)
inactive_user.add_record_check((A.READ,), 'topic', func=check_remove_content_for_select)
normal_user.add_record_check((A.READ,), 'topic', func=check_remove_content_for_select)


# 跳过不可见的板块
# 与 ignore_post_invisible 基本一致
def ignore_hide_board(ability: Ability, user, query: 'SQLQueryInfo'):
    roles = {ability.role} if not user else set(user.roles)
    if roles & {'superuser', 'admin'}:
        return

    if roles & {'inactive_user', 'user', 'wiki_editor'}:
        visible_limit = POST_VISIBLE.ADMIN_ONLY
    else:
        visible_limit = POST_VISIBLE.USER_ONLY

    # TODO: 以后这种请求加cache
    ignored_board_ids = [x.id.tobytes() for x in Board.select(Board.id).where(~(
        (Board.state > POST_STATE.APPLY) &
        (Board.visible > POST_VISIBLE.HIDE) &
        (Board.visible < visible_limit)
    ))]

    query.add_condition('board_id', SQL_OP.NOT_IN, ignored_board_ids)


visitor.add_query_condition('topic', func=ignore_hide_board)
banned_user.add_query_condition('topic', func=ignore_hide_board)
inactive_user.add_query_condition('topic', func=ignore_hide_board)
normal_user.add_query_condition('topic', func=ignore_hide_board)


# 不准其他用户写入当前用户的文章
def check_is_users_post(ability, user, action, record: DataRecord, available_columns: list):
    if user:
        if record.get('user_id') != user.id:
            available_columns.clear()
    return True


normal_user.add_record_check((A.WRITE,), 'topic', func=check_is_users_post)
