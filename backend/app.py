from slim import Application, json_patch
from slim.base.session import MemoryHeaderSession
import config

json_patch.apply()
app = Application(cookies_secret=config.COOKIE_SECRET, session_cls=MemoryHeaderSession,  enable_log=config.DEBUG)
