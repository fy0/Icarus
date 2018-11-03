from slim.base.permission import Ability, A, DataRecord

visitor = Ability(None, {
    'topic': {
        'id': (A.QUERY, A.READ),
        'title': (A.READ,),
        'user_id': (A.QUERY, A.READ),
        'board_id': (A.QUERY, A.READ),
        'time': (A.READ,),
        'state': (A.READ,),

        'edit_time': (A.READ,),
        'edit_count': (A.READ,),
        'last_edit_user_id': (A.READ,),
        'content': (A.READ,),

        'awesome': (A.READ,),
        'sticky_weight': (A.QUERY, A.READ,),
        'weight': (A.READ,),
        'update_time': (A.READ,),
    },
    'wiki_article': {
        'id': (A.QUERY, A.READ),
        'state': (A.READ,),
        'visible': (A.READ,),
        'time': (A.READ,),
        'user_id': (A.QUERY, A.READ),

        'title': (A.READ,),
        'ref': (A.QUERY, A.READ,),
        'content': (A.READ,),
        'flag': (A.QUERY, A.READ,),
    },
    'user': {
        'id': (A.QUERY, A.READ),
        'nickname': (A.READ, A.CREATE),
        'group': (A.READ,),
        'state': (A.READ,),
        'number': (A.READ,),
        'biology': (A.READ,),
        'time': (A.READ,),
        'key_time': (A.READ,),
        'avatar': (A.READ,),
        'type': (A.READ,),
        'url': (A.READ,),
        'location': (A.READ,),

        'email': (A.CREATE,),
        'exp': (A.READ,),
        'credit': (A.READ,),
        'repute': (A.READ,),
    },
    'board': {
        'id': (A.QUERY, A.READ),
        'name': (A.READ,),
        'brief': (A.READ,),
        'desc': (A.READ,),
        'time': (A.READ, A.QUERY,),
        'weight': (A.READ, A.QUERY),
        'color': (A.READ,),
        'state': (A.READ,),
        'visible': (A.READ,),
        'category': (A.READ,),
        'parent_id': (A.QUERY, A.READ,)
    },
    'comment': {
        'id': (A.QUERY, A.READ),
        'related_id': (A.QUERY, A.READ),
        'related_type': (A.QUERY, A.READ),
        'user_id': (A.QUERY, A.READ),
        'reply_to_cmt_id': (A.QUERY, A.READ),
        'time': (A.READ,),
        'state': (A.READ,),
        'visible': (A.READ,),
        'content': (A.READ,),
        'post_number': (A.READ,),
    },
    'statistic': {
        'id': (A.READ, A.QUERY),
        'post_type': (A.READ,),

        'click_count': (A.READ,),
        'comment_count': (A.READ,),
        'topic_count': (A.READ,),
        'last_comment_id': (A.READ,),

        'follow_count': (A.READ,),
    },
    'statistic24h': {
        'id': (A.READ, A.QUERY),
        'post_type': (A.READ,),

        'click_count': (A.READ,),
        'comment_count': (A.READ,),
        'topic_count': (A.READ,),
        'last_comment_id': (A.READ,),

        'follow_count': (A.READ,),
    },
    'manage_log': {
        'id': (A.READ,),
        'user_id': (A.READ,),
        'role': (A.READ,),
        'time': (A.READ,),
        'related_type': (A.READ,),
        'related_id': (A.READ, A.QUERY),
        'operation': (A.READ,),
        'value': (A.READ,),
        'note': (A.READ,)
    }
})
