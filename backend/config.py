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

HOST = '127.0.0.1'
PORT = 9999
DEBUG_LEVEL = logging.DEBUG
DATABASE_URI = 'postgresql://postgres@localhost/icarus'  # 必填

REDIS_URI = 'redis://localhost:6379'

# 为True时，密码将先在前端哈希后，在后端再次哈希与储存值比对。
# 从1.0版升级后，如果开启这个选项，那么现有用户全部需要重置密码
USER_SECURE_AUTH_ENABLE = True
USER_SECURE_AUTH_FRONTEND_SALT = b'6I6r5oSB5YmN6Lev5peg55+l5bex77yM5aSp5LiL6LCB5Lq65LiN6K+G5ZCb'  # 前端盐，务必修改默认值

##########################################
# 可选配置 - 用户昵称、邮箱约束
##########################################
USER_ALLOW_SIGNUP = True  # 开放注册

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
# 可选 - 用户配置
##########################################

USER_RESET_PASSWORD_REQUST_INTERVAL = 30 * 60  # 申请重置密码间隔，默认30分钟
USER_RESET_PASSWORD_CODE_EXPIRE = 12 * 60 * 60  # 重置密码代码有效期，默认12小时

USER_ACTIVATION_REQUEST_INTERVAL = 30 * 60  # 申请激活间隔，默认30分钟
USER_ACTCODE_EXPIRE = 3 * 24 * 60 * 60  # 用户激活代码有效期，默认3天

USER_CHECKIN_COUNTER_INTERVAL = 3 * 24 * 60 * 60  # 签到连击间隔，默认3天

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
# 可选 - 文件上传（七牛配置）
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
PASSWORD_SECURE_HASH_FUNC_NAME = 'sha512'
PASSWORD_SECURE_HASH_ITERATIONS = 10_0000  # 默认密码迭代次数，按2017年报告推荐至少1w次
SESSION_ID_GENERATOR = CustomID

# 被数据库所使用的两个ID，短ID与长ID
POST_ID_GENERATOR = AutoGenerator  # 代表SQL自动生成
LONG_ID_GENERATOR = CustomID

##########################################
# 可选 - 接口冷却时间
##########################################

USER_SIGNIN_COOLDOWN_BY_IP = 10  # 单IP登录间隔时间
USER_SIGNIN_COOLDOWN_BY_ACCOUNT = 10  # 帐户登录间隔时间
USER_SIGNUP_COOLDOWN_BY_IP = 10 * 60  # 单IP注册间隔时间
USER_CHANGE_PASSWORD_COOLDOWN_BY_ACCOUNT = 2 * 60  # 帐户修改密码间隔时间
USER_REQUEST_PASSWORD_RESET_COOLDOWN_BY_IP = 5 * 60  # 重置密码申请时间间隔
USER_REQUEST_PASSWORD_RESET_COOLDOWN_BY_ACCOUNT = 5 * 60  # 重置密码申请时间间隔

TOPIC_NEW_COOLDOWN_BY_IP = 60  # IP发帖间隔：60s
TOPIC_NEW_COOLDOWN_BY_ACCOUNT = 60  # 发帖间隔：60s
COMMENT_NEW_COOLDOWN_BY_IP = 15  # 评论间隔：15s
COMMENT_NEW_COOLDOWN_BY_ACCOUNT = 15  # 评论间隔：15s

##########################################
# 可选 - 其他
##########################################

NOTIF_FETCH_COOLDOWN = 14
MENTION_LIMIT_PER_POST = 20

##########################################
# 其它
##########################################

# 项目使用类 restful 方式进行通信，并未使用cookies，不用管这个值
COOKIES_SECRET = b"6aOO5ZC55LiN5pWj6ZW/5oGo77yM6Iqx5p+T5LiN6YCP5Lmh5oSB44CC"

##########################################
# 加载备用配置
##########################################

try:
    from private import *
except:
    pass
