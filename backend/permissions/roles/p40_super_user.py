from permissions.roles.p30_normal_user import normal_user
from slim.base.permission import Ability, A, DataRecord

super_user = Ability('superuser', {
    'topic': {
        'title': A.ALL,
        'visible': A.ALL,
        'board_id': (A.QUERY, A.READ, A.CREATE, A.WRITE),
        'content': (A.READ, A.CREATE, A.WRITE),
        'awesome': (A.READ, A.WRITE, A.QUERY),
        'weight': (A.QUERY, A.READ, A.WRITE),
        'sticky_weight': (A.READ, A.WRITE),
        'state': A.ALL,
    },
    'wiki_article': {
        'state': A.ALL,
        'visible': A.ALL,

        'title': A.ALL,
        'ref': A.ALL,
        'content': A.ALL,
    },
    'board': {
        'name': A.ALL,
        'brief': A.ALL,
        'desc': A.ALL,
        'time': (A.READ, A.QUERY, A.CREATE,),
        'weight': A.ALL,
        'color': (A.READ, A.WRITE, A.CREATE),
        'state': A.ALL,
        'visible': A.ALL,
        'category': A.ALL,
        'user_id': (A.READ, A.CREATE),
        'parent_id': A.ALL
    },
    'user': {
        'key': (A.WRITE,),
        'time': (A.READ,),
        'state': A.ALL,
        'email': A.ALL,
        'nickname': A.ALL,
        'credit': A.ALL,
        'group': A.ALL,
        'repute': A.ALL
    }
}, based_on=normal_user)
