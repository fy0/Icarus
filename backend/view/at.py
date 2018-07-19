from lib.atsearch import at_replace
from model.user import User


def check_content_with_at(content):
    ncontent, old_at, new_at = at_replace(content, User.nicknames_filter)
    return ncontent
