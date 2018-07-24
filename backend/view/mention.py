import time

import config
from lib.atsearch import at_replace
from model.mention import Mention
from model.user import User


def check_content_mention(content):
    ncontent, matched, data = at_replace(content, User.find_by_nicknames)

    def do_mentions(user_id, mentioned_user_id, related_type, related_id):
        items = []
        for i in data.values():
            items.append({
                'id': config.LONG_ID_GENERATOR().to_bin(),
                'user_id': user_id,
                'time': int(time.time()),
                'who': mentioned_user_id,
                'related_id': related_id,
                'related_type': related_type,
            })

        Mention.insert_many(items).execute()

    return ncontent, do_mentions
