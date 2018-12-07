from permissions.roles.p30_normal_user import normal_user
from slim.base.permission import Ability, A, DataRecord


def merge_post_permissions_of_superuser(d):
    base = {
        'state': (A.QUERY, A.READ, A.WRITE, A.CREATE),
        'visible': (A.QUERY, A.READ, A.WRITE, A.CREATE),
        'time': (A.READ, A.CREATE),
        'user_id': (A.QUERY, A.READ, A.CREATE),
    }
    base.update(d)
    return base


superuser = Ability('superuser', {
    'topic': merge_post_permissions_of_superuser({
        'title': A.ALL,
        'board_id': (A.QUERY, A.READ, A.CREATE, A.WRITE),
        'content': (A.READ, A.CREATE, A.WRITE),
        'awesome': (A.READ, A.WRITE, A.QUERY),
        'weight': (A.QUERY, A.READ, A.WRITE),
        'sticky_weight': (A.READ, A.WRITE),
    }),
    'wiki_article': merge_post_permissions_of_superuser({
        'title': A.ALL,
        'ref': A.ALL,
        'content': A.ALL,
    }),
    'board': merge_post_permissions_of_superuser({
        'name': A.ALL,
        'brief': A.ALL,
        'desc': A.ALL,
        'weight': A.ALL,
        'color': (A.READ, A.WRITE, A.CREATE),
        'category': A.ALL,
        'parent_id': A.ALL,
        'can_post_rank': A.ALL,
    }),
    'user': merge_post_permissions_of_superuser({
        'key': (A.WRITE,),
        'password': (A.WRITE,),
        'email': A.ALL,
        'nickname': A.ALL,
        'credit': A.ALL,
        'repute': A.ALL,
        'key_time': (A.READ,),
        'access_time': (A.READ,),
        'last_check_in_time': (A.READ,),

        'is_wiki_editor': (A.QUERY, A.READ, A.WRITE,),
        'is_board_moderator': (A.QUERY, A.READ, A.WRITE,),
        'is_forum_master': (A.QUERY, A.READ, A.WRITE,),
    })
}, based_on=normal_user)
