from slim.base.permission import Ability, A, AbilityRecord

visitor = Ability(None, {
    'topic': {
        'id': [A.QUERY, A.READ],
        'title': [A.READ],
        'user_id': [A.QUERY, A.READ],
        'board_id': [A.QUERY, A.READ],
        'time': [A.READ],
        'state': [A.READ],

        'edit_time': [A.READ],
        'last_edit_user_id': [A.READ],
        'content': [A.READ],

        'sticky_weight': [A.READ],
        'weight': [A.READ],
    },
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
    },
    'topic': {
        'title': [A.READ, A.CREATE, A.WRITE],
        'board_id': [A.QUERY, A.READ, A.CREATE, A.WRITE],
        'content': [A.READ, A.CREATE, A.WRITE],
    }
}, based_on=visitor)

super_user = Ability('superuser', {
    'topic': {
        'title': A.ALL,
        'board_id': [A.QUERY, A.READ, A.CREATE, A.WRITE],
        'content': [A.READ, A.CREATE, A.WRITE],
    },
    'board': {
        'name': A.ALL,
        'brief': A.ALL,
        'desc': A.ALL,
        'time': (A.READ, A.QUERY, A.CREATE,),
        'weight': A.ALL,
        'color': (A.READ, A.WRITE, A.CREATE),
        'state': A.ALL,
        'category': A.ALL
    }
}, based_on=normal_user)

admin = Ability('admin', {
    'topic': {
        'title': A.ALL,
        'board_id': [A.QUERY, A.READ, A.CREATE, A.WRITE],
        'content': [A.READ, A.CREATE, A.WRITE],
        'state': A.ALL,
    },
    'user': {
        'email': A.ALL,
        'nickname': A.ALL,
        'group': A.ALL,
        'state': A.ALL,
        'credit': A.ALL,
        'reputation': A.ALL
    }
}, based_on=super_user)


# user


def user_check(ability, user, action, record: AbilityRecord, available_columns: list):
    if user and record.get('id') == user.id:
        available_columns.append('email')
    return True


normal_user.add_record_check([A.READ], 'user', func=user_check)

# topic


def is_users_post(ability, user, action, record: AbilityRecord, available_columns: list):
    if user:
        if record.get('user_id') != user.id:
            available_columns.clear()
    return True


normal_user.add_record_check((A.WRITE,), 'topic', func=is_users_post)
