from slim import Application, json_patch
import config

json_patch.apply()
app = Application(cookies_secret=config.COOKIE_SECRET, enable_log=config.DEBUG)
