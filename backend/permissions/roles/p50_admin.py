from permissions.roles.p40_super_user import superuser
from slim.base.permission import Ability, A, DataRecord

admin = Ability({
    'user': {
        'group': A.ALL,
    }
}, based_on=superuser)
