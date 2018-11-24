from permissions.roles import *
from permissions.tables import *


def permissions_add_all(permission):
    permission.add(visitor)
    permission.add(banned_user)
    permission.add(inactive_user)
    permission.add(normal_user)
    permission.add(wiki_editor)
    permission.add(superuser)
    permission.add(admin)
