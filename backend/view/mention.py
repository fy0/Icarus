import time

import config
from lib.atsearch import at_replace
from model.mention import Mention
from model.user import User


def check_content_mention(content):
    ncontent, matched, mentioned_users = at_replace(content, User.find_by_nicknames)

    def do_mentions(sender_id, loc_title, location, related, data=None):
        """
        :param sender_id:
        :param loc_title: 地点标题
        :param location: [post_type, post_id] 形式，指向事件发生的主要地点，例如文章中的评论里@，主要地点是文章
        :param related: [post_type, post_id] 形式，指向事件发生的准确地点，例如文章中的评论里@，主要地点是评论
        :param data:
        :return:
        """
        items = []
        t = int(time.time())

        for i in mentioned_users.values():
            i: User
            if i.id == sender_id:
                continue
            items.append({
                'id': config.LONG_ID_GENERATOR().to_bin(),
                'user_id': sender_id,
                'time': t,
                'who': i.id,

                'loc_post_type': location[0],
                'loc_post_id': location[1],
                'loc_post_title': loc_title,

                'related_type': related[0],
                'related_id': related[1],

                'data': data,
            })

        if not items: return
        Mention.insert_many(items).execute()

    return ncontent, do_mentions
