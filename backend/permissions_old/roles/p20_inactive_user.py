# deprecated
from slim.tools.migrate._permission import A, Ability, role_convert
from permissions_old.roles.p10_visitor import visitor


inactive_user = Ability({
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
