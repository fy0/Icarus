import time
import qiniu
import config

q = None


def init():
    global q
    if config.UPLOAD_ENABLE:
        q = qiniu.Auth(config.UPLOAD_QINIU_ACCESS_KEY, config.UPLOAD_QINIU_SECRET_KEY)


def get_token(user_id=None):
    token = q.upload_token(config.UPLOAD_QINIU_BUCKET, policy={
        'scope': config.UPLOAD_QINIU_BUCKET,
        'saveKey': config.UPLOAD_QINIU_SAVEKEY,
        'deadline': int(time.time()) + config.UPLOAD_QINIU_DEADLINE_OFFSET,
        # 'callbackUrl': '',
        # 'callbackHost': '1',
        'callbackBodyType': 'application/json',
        'fsizeMin': config.UPLOAD_FILE_SIZE_MIN,
        'fsizeLimit': config.UPLOAD_FILE_SIZE_MAX,
        'mimeLimit': config.UPLOAD_FILE_SIZE_MIN,
        'endUser': user_id,
    })
    return token


def upload_local(token, data, key=None):
    return qiniu.put_data(token, key, data)
