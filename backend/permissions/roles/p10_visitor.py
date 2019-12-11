from slim.base.permission import Ability, A, DataRecord


def merge_post_permissions_of_visitor(d):
    """
    所有 post 均有的5个值
    :param d:
    :return:
    """
    base = {
        'id': (A.QUERY, A.READ),
        'state': (A.READ,),
        'visible': (A.READ,),
        'time': (A.READ,),
        'user_id': (A.QUERY, A.READ),
    }
    base.update(d)
    return base


visitor = Ability({
    'topic': merge_post_permissions_of_visitor({
        'title': (A.READ,),
        'board_id': (A.QUERY, A.READ),

        'edit_count': (A.READ,),
        'edit_time': (A.READ,),
        'last_edit_user_id': (A.READ,),
        'content': (A.READ,),

        'awesome': (A.READ,),
        'sticky_weight': (A.QUERY, A.READ,),
        'weight': (A.READ,),
        'update_time': (A.READ,),
    }),
    'wiki_article': merge_post_permissions_of_visitor({
        'title': (A.READ,),
        'ref': (A.QUERY, A.READ,),
        'content': (A.READ,),
        'flag': (A.QUERY, A.READ,),
    }),
    'user': merge_post_permissions_of_visitor({
        'email': (A.CREATE,),
        'phone': (A.CREATE,),
        'nickname': (A.READ, A.CREATE),

        'biology': (A.READ,),
        'avatar': (A.READ,),
        'type': (A.READ,),
        'url': (A.READ,),
        'location': (A.READ,),
        'group': (A.READ,),

        'is_wiki_editor': (A.READ,),
        'is_board_moderator': (A.READ,),
        'is_forum_master': (A.READ,),

        'access_time': (A.READ,),
        'number': (A.READ,),
        'exp': (A.READ,),
        'credit': (A.READ,),
        'repute': (A.READ,),
    }),
    'board': merge_post_permissions_of_visitor({
        'name': (A.READ,),
        'brief': (A.READ,),
        'desc': (A.READ,),
        'weight': (A.READ, A.QUERY),
        'color': (A.READ,),
        'category': (A.READ,),
        'parent_id': (A.QUERY, A.READ,),
        'can_post_rank': (A.QUERY, A.READ,),
    }),
    'comment': merge_post_permissions_of_visitor({
        'related_id': (A.QUERY, A.READ),
        'related_type': (A.QUERY, A.READ),
        'reply_to_cmt_id': (A.QUERY, A.READ),
        'content': (A.READ,),
        'post_number': (A.READ,),
    }),

    # 以下并非post类型
    'post_stats': {
        '*': {A.READ},
        'id': (A.READ, A.QUERY),
    },
    'manage_log': {
        '*': {A.READ},
        'related_type': (A.READ, A.QUERY),
        'related_id': (A.READ, A.QUERY),
    }
})
