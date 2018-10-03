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

    asyncio.ensure_future(redis_init(loop), loop=loop)

    if config.UPLOAD_ENABLE:
        upload.init()

    app.run(host=config.HOST, port=config.PORT)
