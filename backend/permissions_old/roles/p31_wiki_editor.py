from permissions_old.roles.p30_normal_user import normal_user
from permissions_old.roles.p40_super_user import merge_post_permissions_of_superuser
from slim.tools.migrate._permission import A, Ability


wiki_editor = Ability({
    'wiki_article': merge_post_permissions_of_superuser({
        'title': A.ALL,
        'ref': A.ALL,
        'content': A.ALL,
    }),
}, based_on=normal_user)
