from slim import app_init
from aiohttp import web

from view import route
import model.models
import config

app = app_init(config.COOKIE_SECRET, enable_log=config.DEBUG, route=route)
web.run_app(app, host=config.HOST, port=config.PORT)
