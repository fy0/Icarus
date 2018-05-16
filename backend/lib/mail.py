import aiosmtplib
from email.mime.text import MIMEText
import config

smtp = None


async def init(loop):
    global smtp
    smtp = aiosmtplib.SMTP(hostname=config.EMAIL_HOST, port=config.EMAIL_PORT, loop=loop, use_tls=config.EMAIL_USE_TLS)
    await smtp.connect()
    await smtp.login(config.EMAIL_USERNAME, config.EMAIL_PASSWORD)


async def try_reconnect():
    global smtp

    try:
        await smtp.helo()
    except aiosmtplib.SMTPServerDisconnected:
        # smtp.is_connected 本来有个这个，但经测试并不管用，只在触发异常后被重置，而不能主动探测。
        await smtp.connect()
        await smtp.login(config.EMAIL_USERNAME, config.EMAIL_PASSWORD)


async def send(to, title, content):
    await try_reconnect()
    message = MIMEText(content)
    message['From'] = '%s <%s>' % (config.EMAIL_SENDER, config.EMAIL_USERNAME)
    message['To'] = to
    message['Subject'] = title
    await smtp.send_message(message)
