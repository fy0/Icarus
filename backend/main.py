import misc.setup
import asyncio
from app import app
from lib import mail
from model.redis import init as redis_init
from slim.utils import get_ioloop
import config

if __name__ == '__main__':
    import model._models
    import api._views
    import permissions

    async def on_startup():
        loop = get_ioloop()

        if config.EMAIL_ENABLE:
            asyncio.ensure_future(mail.init(loop), loop=loop)

        await redis_init(loop)

        if config.UPLOAD_ENABLE:
            if config.UPLOAD_BACKEND == 'qiniu':
                from lib import qn
                qn.init()

    app.on_startup.append(on_startup)
    app.run(host=config.HOST, port=config.PORT)
