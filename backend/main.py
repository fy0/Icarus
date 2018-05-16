import asyncio
from app import app
from lib import mail
import config

if __name__ == '__main__':
    import model._models
    import view._views
    loop = asyncio.get_event_loop()
    loop.run_until_complete(mail.init(loop))
    app.run(host=config.HOST, port=config.PORT)
