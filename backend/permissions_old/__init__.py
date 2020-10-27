from permissions_old.roles.p10_visitor import visitor
from permissions_old.roles.p11_banned_user import banned_user
from permissions_old.roles.p20_inactive_user import inactive_user
from permissions_old.roles.p30_normal_user import normal_user
from permissions_old.roles.p31_wiki_editor import wiki_editor
from permissions_old.roles.p40_super_user import superuser
from permissions_old.roles.p50_admin import admin
from slim.tools.migrate._permission import role_convert


role_convert(visitor, 'visitor')
role_convert(banned_user, 'banned_user', 'visitor')
role_convert(inactive_user, 'inactive_user', based_on_name='visitor')
role_convert(normal_user, 'normal_user', based_on_name='inactive_user')
role_convert(wiki_editor, 'wiki_editor', based_on_name='normal_user')
role_convert(superuser, 'super_user', based_on_name='normal_user')
role_convert(admin, 'admin', based_on_name='super_user')
