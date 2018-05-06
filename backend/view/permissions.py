from model.post import POST_STATE, POST_VISIBLE
from slim.base.permission import Ability, A, DataRecord
from slim.base.sqlquery import SQLQueryInfo

visitor = Ability(None, {
    'topic': {
        'id': (A.QUERY, A.READ),
        'title': (A.READ,),
        'user_id': (A.QUERY, A.READ),
        'board_id': (A.QUERY, A.READ),
        'time': (A.READ,),
        'state': (A.READ,),

        'edit_time': (A.READ,),
        'edit_count': (A.READ,),
        'last_edit_user_id': (A.READ,),
        'content': (A.READ,),

        'awesome': (A.READ,),
        'sticky_weight': (A.READ,),
        'weight': (A.READ,),
    },
    'user': {
        'id': (A.QUERY, A.READ),
        'nickname': (A.READ, A.CREATE),
        'group': (A.READ,),
        'number': (A.READ,),
        'biology': (A.READ,),
        'reg_time': (A.READ,),
        'key_time': (A.READ,),

        'email': (A.CREATE,),
    },
    'board': {
        'id': (A.QUERY, A.READ),
        'name': (A.READ,),
        'brief': (A.READ,),
        'desc': (A.READ,),
        'time': (A.READ, A.QUERY,),
        'weight': (A.READ, A.QUERY),
        'color': (A.READ,),
        'state': (A.READ,),
        'category': (A.READ,),
        'parent_id': (A.QUERY, A.READ,)
    },
    'comment': {
        'id': (A.QUERY, A.READ),
        'related_id': (A.QUERY, A.READ),
        'related_type': (A.QUERY, A.READ),
        'user_id': (A.QUERY, A.READ),
        'reply_to_cmt_id': (A.QUERY, A.READ),
        'time': (A.READ,),
        'state': (A.READ,),
        'visible': (A.READ,),
        'content': (A.READ,),
    },
    'statistic': {
        'id': (A.READ, A.QUERY),
        'post_type': (A.READ,),

        'click_count': (A.READ,),
        'comment_count': (A.READ,),
        'topic_count': (A.READ,),
        'last_comment_id': (A.READ,),

        'follow_count': (A.READ,),
    },
    'statistic24h': {
        'id': (A.READ, A.QUERY),
        'post_type': (A.READ,),

        'click_count': (A.READ,),
        'comment_count': (A.READ,),
        'topic_count': (A.READ,),
        'last_comment_id': (A.READ,),

        'follow_count': (A.READ,),
    },
})

normal_user = Ability('user', {
    'user': {
        'nickname': (A.QUERY, A.READ, A.WRITE),
        'group': (A.READ,),
        # 'key': ['query', 'read']
    },
    'topic': {
        'title': (A.READ, A.CREATE, A.WRITE),
        'board_id': (A.QUERY, A.READ, A.CREATE),
        'content': (A.READ, A.CREATE, A.WRITE),
    },
    'comment': {
        'related_id': (A.READ, A.CREATE,),
        'related_type': (A.READ, A.CREATE,),
        'reply_to_cmt_id': (A.READ, A.CREATE,),
        'state': (A.READ, A.WRITE,),
        'content': (A.READ, A.CREATE,),
    },
}, based_on=visitor)

super_user = Ability('superuser', {
    'topic': {
        'title': A.ALL,
        'board_id': (A.QUERY, A.READ, A.CREATE, A.WRITE),
        'content': (A.READ, A.CREATE, A.WRITE),
        'awesome': (A.READ, A.WRITE, A.QUERY),
        'weight': (A.QUERY, A.READ, A.WRITE),
        'sticky_weight': (A.READ, A.WRITE),
        'state': A.ALL,
    },
    'board': {
        'name': A.ALL,
        'brief': A.ALL,
        'desc': A.ALL,
        'time': (A.READ, A.QUERY, A.CREATE,),
        'weight': A.ALL,
        'color': (A.READ, A.WRITE, A.CREATE),
        'state': A.ALL,
        'category': A.ALL,
        'creator_id': (A.READ, A.CREATE),
        'parent_id': A.ALL
    },
    'user': {
        'key': (A.WRITE,),
        'reg_time': (A.READ,),
        'state': (A.READ,),
        'email': A.ALL,
        'nickname': A.ALL,
        'credit': A.ALL,
        'group': A.ALL,
        'reputation': A.ALL
    }
}, based_on=normal_user)

admin = Ability('admin', {
    'user': {
        'group': A.ALL,
    }
}, based_on=super_user)


# user

def user_check(ability, user, action, record: DataRecord, available_columns: list):
    if user and record.get('id') == user.id:
        available_columns.append('email')
    return True


normal_user.add_record_check([A.READ], 'user', func=user_check)

# topic

visitor.add_query_condition('topic', [
    ('state', '>', POST_VISIBLE.HIDE),
    ('state', '<', POST_VISIBLE.USER_ONLY),
])

visitor.add_query_condition('board', [
    ('state', '>', POST_VISIBLE.HIDE),
])


def check_remove_content_for_select(ability, user, action, record: DataRecord, available_columns: list):
    if user:
        if record.get('state') == POST_VISIBLE.CONTENT_IF_LOGIN:
            available_columns.remove('content')
    return True


visitor.add_record_check((A.READ,), 'topic', func=check_remove_content_for_select)

normal_user.add_query_condition('topic', [
    ('state', '>', POST_VISIBLE.HIDE),
    ('state', '<', POST_VISIBLE.ADMIN_ONLY),
])

normal_user.add_query_condition('board', [
    ('state', '>', POST_VISIBLE.HIDE),
])


def check_is_users_post(ability, user, action, record: DataRecord, available_columns: list):
    if user:
        if record.get('user_id') != user.id:
            available_columns.clear()
    return True


normal_user.add_record_check((A.WRITE,), 'topic', func=check_is_users_post)
