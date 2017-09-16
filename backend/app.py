from slim import app_init
from slim.utils import json_patch
from aiohttp import web
from view import route
import model.models
import view.views
import config

json_patch.apply()
app = app_init(config.COOKIE_SECRET, enable_log=config.DEBUG, route=route)
web.run_app(app, host=config.HOST, port=config.PORT)
