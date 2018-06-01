import json
import time
import qiniu
import config

q = None


def init():
    global q
    q = qiniu.Auth(config.UPLOAD_QINIU_ACCESS_KEY, config.UPLOAD_QINIU_SECRET_KEY)


def get_token(user_id=None, type_name=None):
    if not config.UPLOAD_ENABLE: return
    empty = 'null'
    token = q.upload_token(config.UPLOAD_QINIU_BUCKET, policy={
        'scope': config.UPLOAD_QINIU_BUCKET,
        'saveKey': config.UPLOAD_QINIU_SAVEKEY,
        'deadline': int(time.time()) + config.UPLOAD_QINIU_DEADLINE_OFFSET,
        'callbackUrl': config.UPLOAD_QINIU_CALLBACK_URL,
        # 'callbackBody': json.dumps({"key": "$(key)", "hash": "$(etag)",
        #                  "w": "$(imageInfo.width)", "h": "$(imageInfo.height)"}),
        # 'callbackBodyType': 'application/json',
        'callbackBody': 'key=$(key)&hash=$(etag)&w=$(imageInfo.width)&h=$(imageInfo.height)'
                        f'&user_id={user_id or empty}&type_name={type_name or empty}',
        'fsizeMin': config.UPLOAD_FILE_SIZE_MIN,
        'fsizeLimit': config.UPLOAD_FILE_SIZE_MAX,
        'mimeLimit': config.UPLOAD_QINIU_MIME_LIMIT,
        'endUser': user_id,
    })
    return token


def verify_callback(auth, url, body):
    if not config.UPLOAD_ENABLE: return
    return q.verify_callback(auth, url, body)


def upload_local(token, data, key=None):
    if not config.UPLOAD_ENABLE: return
    return qiniu.put_data(token, key, data)


if __name__ == '__main__':
    init()
    t = get_token()
    print(upload_local(t, open('test.png', 'rb').read(), None))
