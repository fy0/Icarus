import asyncio
from app import app
from lib import mail, upload
import config

if __name__ == '__main__':
    import model._models
    import view._views

    if config.EMAIL_ENABLE:
        loop = asyncio.get_event_loop()
        asyncio.ensure_future(mail.init(loop), loop=loop)

    if config.UPLOAD_ENABLE:
        upload.init()

    app.run(host=config.HOST, port=config.PORT)
