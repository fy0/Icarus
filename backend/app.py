from slim import Application, CORSOptions, EMPTY_PERMISSION
from slim.base.session import MemoryHeaderKeySession
import config

app = Application(
    cookies_secret=config.COOKIES_SECRET,
    session_cls=MemoryHeaderKeySession,
    permission=EMPTY_PERMISSION,
    log_level=config.DEBUG_LEVEL,
    cors_options=config.CORS_OPTIONS
)
