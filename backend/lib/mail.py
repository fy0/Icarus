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
    message = MIMEText(content, 'html', 'utf-8')
    message['From'] = '%s <%s>' % (config.EMAIL_SENDER, config.EMAIL_USERNAME)
    message['To'] = to
    message['Subject'] = title
    return await smtp.send_message(message)


async def send_register_activation(user):
    act_code = user.get_activation_code()
    act_url = f'{config.SITE_URL}/api/user/active?uid={user.id.hex()}&code={act_code}'

    content = f'''Email 地址验证<br/><br/>

您好，{user.nickname}。<br/>
欢迎来到 {config.SITE_NAME} 社区。<br/><br/>

您收到这封邮件，是由于在 {config.SITE_NAME} 进行了新用户注册，或用户修改 Email 使用了这个邮箱地址。<br/>
如果您并没有访问过 {config.SITE_NAME}，或没有进行上述操作，请忽略这封邮件。<br/><br/>

如果您进行了新用户注册，或者修改 Email 使用了这个邮箱地址，我们需要对您的地址有效性进行验证以避免垃圾邮件或地址被滥用。<br/><br/>

点击下面的链接激活账号：<br/>
<a href="{act_url}" target="_blank">{act_url}</a><br/>
（如果上面不是链接形式，请将该地址手工复制到浏览器地址栏中打开以完成验证）<br/><br/>

考虑到安全问题，此链接在72个小时内有效。<br/>
感谢您的访问，祝您使用愉快！<br/><br/>

此致，<br/>
{config.SITE_NAME} 管理团队<br/>
{config.SITE_URL}<br/>
'''

    return await send(f'{user.nickname} <{user.email}>', f'[{config.SITE_NAME}] Email 地址验证', content)
