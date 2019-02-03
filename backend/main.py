import misc.setup
import asyncio
from app import app
from lib import mail, qn
from model.redis import init as redis_init
from slim.utils import get_ioloop
import config

if __name__ == '__main__':
    import model._models
    import view._views
    import permissions

    loop = get_ioloop()
    if config.EMAIL_ENABLE:
        asyncio.ensure_future(mail.init(loop), loop=loop)

    co_redis = redis_init(loop)
    loop.run_until_complete(co_redis)

    if config.UPLOAD_ENABLE:
        qn.init()

    app.run(host=config.HOST, port=config.PORT)
