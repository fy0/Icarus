from permissions.roles.p40_super_user import super_user
from slim.base.permission import Ability, A, DataRecord

admin = Ability('admin', {
    'user': {
        'group': A.ALL,
    }
}, based_on=super_user)
