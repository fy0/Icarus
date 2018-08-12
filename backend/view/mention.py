import time

import config
from lib.atsearch import at_replace
from model.mention import Mention
from model.user import User


def check_content_mention(content):
    ncontent, matched, mentioned_users = at_replace(content, User.find_by_nicknames)

    def do_mentions(sender_id, related_type, related_id, data):
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
                'related_id': related_id,
                'related_type': related_type,
                'data': data,
            })

        if not items: return
        Mention.insert_many(items).execute()

    return ncontent, do_mentions
