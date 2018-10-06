import misc.setup
import asyncio
from app import app
from lib import mail, upload
from model.redis import init as redis_init
from slim.utils import get_ioloop
import config

if __name__ == '__main__':
    import model._models
    import view._views

    loop = get_ioloop()
    if config.EMAIL_ENABLE:
        asyncio.ensure_future(mail.init(loop), loop=loop)

    co_redis = redis_init(loop)
    asyncio.ensure_future(co_redis, loop=loop)

    if config.UPLOAD_ENABLE:
        upload.init()

    asyncio.wait_for(co_redis, 10000, loop=loop)
    app.run(host=config.HOST, port=config.PORT)
