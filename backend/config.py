import hashlib

from lib.customid import CustomID
from slim.utils import ObjectID

PROJECT_NAME = 'Icarus'
VERSION = '1.0.0'

HOST = '0.0.0.0'
PORT = 9999
DEBUG = True
DATABASE_URI = 'postgresql://postgres@localhost/icarus'
COOKIE_SECRET = b"6aOO5ZC55LiN5pWj6ZW/5oGo77yM6Iqx5p+T5LiN6YCP5Lmh5oSB44CC"

REDIS_HOST = 'localhost'
REDIS_PORT = 6378

USER_ALLOW_SIGNUP = True

PASSWORD_HASH_FUNC = hashlib.sha256
ID_GENERATOR = CustomID

try:
    from private import *
except:
    pass
