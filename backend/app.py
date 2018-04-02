from slim import Application
from slim.base.session import MemoryHeaderSession
import config

app = Application(
    cookies_secret=config.COOKIE_SECRET,
    session_cls=MemoryHeaderSession,
    log_level=config.DEBUG
)
