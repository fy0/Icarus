from slim import Application, CORSOptions
from slim.base.session import MemoryHeaderKeySession
import config

app = Application(
    cookies_secret=config.COOKIE_SECRET,
    session_cls=MemoryHeaderKeySession,
    log_level=config.DEBUG,
    cors_options=CORSOptions('*', allow_credentials=True, expose_headers="*", allow_headers="*")
)
