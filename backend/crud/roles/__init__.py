from crud.roles.r10_vistor import visitor
from crud.roles.r11_banned_user import banned_user
from crud.roles.r20_inactive_user import inactive_user
from crud.roles.r30_normal_user import normal_user
from crud.roles.r31_wiki_editor import wiki_editor
from crud.roles.r40_super_user import super_user
from crud.roles.r50_admin import admin

ordinary_roles = {visitor, banned_user, inactive_user, normal_user, wiki_editor}
admin_roles = {wiki_editor, super_user}
root_roles = {admin}
