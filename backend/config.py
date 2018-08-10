import hashlib
import binascii
import logging
from slim.utils import ObjectID
from slim.utils import CustomID

##########################################
# 必填部分
##########################################

SITE_NAME = 'Icarus'  # 站点名称
SITE_URL = 'http://localhost:8080'  # 必填，站点地址，末尾不要带 /

HOST = '0.0.0.0'
PORT = 9999
DEBUG = logging.DEBUG
DATABASE_URI = 'postgresql://postgres@localhost/icarus'  # 必填
COOKIE_SECRET = b"6aOO5ZC55LiN5pWj6ZW/5oGo77yM6Iqx5p+T5LiN6YCP5Lmh5oSB44CC"  # 必填，务必修改默认值

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

##########################################
# 可选配置 - 用户昵称、邮箱约束
##########################################
USER_ALLOW_SIGNUP = True  # 开放注册

CLIENT_ID = '1b5caadeac09427e7570'
CLIENT_SECRET = 'ea478414584c80d57cd1c9475cd9be2c9625e65d'

def _nickname_checker(username):
    # 被禁止的用户名，此函数仅为示例
    if username not in {'_icarus', }:
        return True


USER_EMAIL_MAX = 128

USER_NICKNAME_MIN = 2
USER_NICKNAME_MAX = 32

USER_NICKNAME_CN_FOR_REG_MIN = 2
USER_NICKNAME_FOR_REG_MIN = 4
USER_NICKNAME_FOR_REG_MAX = 32
USER_NICKNAME_CHECK_FUNC = _nickname_checker

USER_PASSWORD_MIN = 6
USER_PASSWORD_MAX = 128

##########################################
# 可选 - 主题标题与正文限制
##########################################

TOPIC_TITLE_LENGTH_MIN = 3
TOPIC_TITLE_LENGTH_MAX = 50
TOPIC_CONTENT_LENGTH_MAX = 60000

##########################################
# 可选 - 邮件发送配置，默认关闭注册邮件
##########################################

EMAIL_ENABLE = False
EMAIL_ACTIVATION_ENABLE = False
EMAIL_SENDER = 'Icarus 社区程序'
EMAIL_HOST = 'smtp.xxx.com'
EMAIL_PORT = 465
EMAIL_USE_TLS = True
EMAIL_USERNAME = 'user'
EMAIL_PASSWORD = 'pasword'


##########################################
# 可选 - 文件上传
##########################################

UPLOAD_ENABLE = False
UPLOAD_STATIC_HOST = ''
UPLOAD_QINIU_ACCESS_KEY = 'PLACE_HOLDER'
UPLOAD_QINIU_SECRET_KEY = 'PLACE_HOLDER'
UPLOAD_QINIU_BUCKET = 'PLACE_HOLDER'
UPLOAD_QINIU_SAVEKEY = '$(etag)'
UPLOAD_QINIU_DEADLINE_OFFSET = 3600  # 上传key有效时间 10分钟
UPLOAD_QINIU_MIME_LIMIT = 'image/*'
UPLOAD_QINIU_CALLBACK_URL = 'PLACE_HOLDER'  # 开启时必填，七牛上传回调地址
UPLOAD_FILE_SIZE_MIN = 100
UPLOAD_FILE_SIZE_MAX = 3 * 1024 * 1024

##########################################
# 可选 - ID生成器配置
##########################################


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

##########################################
# 可选 - 其他
##########################################

NOTIF_FETCH_COOLDOWN = 14
MENTION_LIMIT_PER_POST = 20

##########################################
# 加载备用配置
##########################################

try:
    from private import *
except:
    pass
