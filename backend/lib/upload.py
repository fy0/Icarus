import time
import qiniu
import config

q = None


def init():
    global q
    q = qiniu.Auth(config.UPLOAD_QINIU_ACCESS_KEY, config.UPLOAD_QINIU_SECRET_KEY)


def get_token(user_id=None):
    if not config.UPLOAD_ENABLE: return
    token = q.upload_token(config.UPLOAD_QINIU_BUCKET, policy={
        'scope': config.UPLOAD_QINIU_BUCKET,
        'saveKey': config.UPLOAD_QINIU_SAVEKEY,
        'deadline': int(time.time()) + config.UPLOAD_QINIU_DEADLINE_OFFSET,
        # 'callbackUrl': '',
        # 'callbackHost': '1',
        'callbackBody': {"key": "$(key)", "hash": "$(etag)",
                         "w": "$(imageInfo.width)", "h": "$(imageInfo.height)"},
        'callbackBodyType': 'application/json',
        'fsizeMin': config.UPLOAD_FILE_SIZE_MIN,
        'fsizeLimit': config.UPLOAD_FILE_SIZE_MAX,
        'mimeLimit': config.UPLOAD_QINIU_MIME_LIMIT,
        'endUser': user_id,
    })
    return token


def upload_local(token, data, key=None):
    if not config.UPLOAD_ENABLE: return
    return qiniu.put_data(token, key, data)


if __name__ == '__main__':
    init()
    t = get_token()
    print(upload_local(t, open('test.png', 'rb').read(), None))
