from permissions.roles.p30_normal_user import normal_user
from permissions.roles.p40_super_user import merge_post_permissions_of_superuser
from slim.base.permission import Ability, A, DataRecord


wiki_editor = Ability('wiki_editor', {
    'wiki_article': merge_post_permissions_of_superuser({
        'title': A.ALL,
        'ref': A.ALL,
        'content': A.ALL,
    }),
}, based_on=normal_user)
