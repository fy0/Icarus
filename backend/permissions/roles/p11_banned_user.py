from slim.base.permission import Ability, A
from permissions.roles.p10_visitor import visitor

# 除了访问自己的用户信息之外，与visitor平权
banned_user = Ability({
    'user': {
        'nickname': (A.QUERY, A.READ),
        'group': (A.READ,),
        'access_time': (A.READ,),
        'last_check_in_time': (A.READ,),
        'check_in_his': (A.READ,),
        # 'key': ['query', 'read']
    },
    'notif': {
        'receiver_id': (A.QUERY, A.READ)
    }
}, based_on=visitor)
