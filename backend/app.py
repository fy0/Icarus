from slim import Application, CORSOptions
from slim.base.session import MemoryHeaderKeySession
import config

app = Application(
    cookies_secret=config.COOKIES_SECRET,
    session_cls=MemoryHeaderKeySession,
    log_level=config.DEBUG_LEVEL,
    cors_options=CORSOptions('*', allow_credentials=True, expose_headers="*", allow_headers="*")
)
