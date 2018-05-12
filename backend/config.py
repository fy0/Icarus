import hashlib
import binascii
import logging
from slim.utils import ObjectID
from slim.utils import CustomID

PROJECT_NAME = 'Icarus'
VERSION = '1.0.0'

HOST = '0.0.0.0'
PORT = 9999
DEBUG = logging.DEBUG
DATABASE_URI = 'postgresql://postgres@localhost/icarus'
COOKIE_SECRET = b"6aOO5ZC55LiN5pWj6ZW/5oGo77yM6Iqx5p+T5LiN6YCP5Lmh5oSB44CC"

REDIS_HOST = 'localhost'
REDIS_PORT = 6378

USER_ALLOW_SIGNUP = True
NOTIF_FETCH_COOLDOWN = 14

EMAIL_MAX = 128


def _nickname_checker(username):
    # 被禁止的用户名
    if username not in {'_icarus', }:
        return True


NICKNAME_MIN = 2
NICKNAME_MAX = 32

NICKNAME_CN_FOR_REG_MIN = 2
NICKNAME_FOR_REG_MIN = 4
NICKNAME_FOR_REG_MAX = 32
NICKNAME_CHECK_FUNC = _nickname_checker

PASSWORD_MIN = 6
PASSWORD_MAX = 128

TOPIC_TITLE_LENGTH_MIN = 3
TOPIC_TITLE_LENGTH_MAX = 50
TOPIC_CONTENT_LENGTH_MAX = 60000


class AutoGenerator:
    def __init__(self, val=b''):
        if isinstance(val, str):
            val = binascii.unhexlify(val)
        self.val = val

    def to_bin(self):
        return self.val


PASSWORD_HASH_FUNC = hashlib.sha256
SESSION_ID_GENERATOR = CustomID

# 被数据库所使用的两个ID，短ID与长ID
POST_ID_GENERATOR = AutoGenerator  # 代表SQL自动生成
LONG_ID_GENERATOR = CustomID

try:
    from private import *
except:
    pass
