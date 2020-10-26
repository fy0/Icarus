from permissions_old.roles.p40_super_user import superuser
from slim.tools.migrate._permission import A, Ability

admin = Ability({
    'user': {
        'group': A.ALL,
    }
}, based_on=superuser)
