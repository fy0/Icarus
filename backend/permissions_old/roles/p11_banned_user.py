from permissions_old import visitor
from slim.tools.migrate._permission import A, Ability

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
