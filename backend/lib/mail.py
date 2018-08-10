import asyncio
import aiosmtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
import async_timeout
from slim.utils import to_hex

import config

smtp = None
curloop = None


async def init(loop):
    global smtp, curloop
    curloop = loop
    try:
        smtp = aiosmtplib.SMTP(hostname=config.EMAIL_HOST, port=config.EMAIL_PORT, loop=loop, use_tls=config.EMAIL_USE_TLS)
        await smtp.connect()
        await smtp.login(config.EMAIL_USERNAME, config.EMAIL_PASSWORD)
        return True
    except aiosmtplib.SMTPConnectError:
        pass


async def try_reconnect():
    try:
        await smtp.helo()
        return True
    except (aiosmtplib.SMTPServerDisconnected, AssertionError):
        # AssertionError: Client not connected 另外还遇到了这个异常
        # smtp.is_connected 本来有个这个，但经测试并不管用，只在触发异常后被重置，而不能主动探测。
        times = 3
        while times:
            try:
                async with async_timeout.timeout(10):
                    print('Email reconnect', times)
                    # 经测试如果不重新生成smtp对象，有可能陷入无限期connect，timeout对其无效
                    if await init(curloop):
                        return True
            except asyncio.TimeoutError:
                times -= 1


async def send(to, title, content):
    if not curloop: return
    if not await try_reconnect(): return
    # smtp: aiosmtplib.SMTP
    message = MIMEText(content, 'html', 'utf-8')
    message['From'] = formataddr((Header(config.EMAIL_SENDER, 'utf-8').encode(), config.EMAIL_USERNAME))
    message['To'] = to
    message['Subject'] = title
    return await smtp.send_message(message)


async def send_register_activation(user):
    act_code = to_hex(user.get_activation_code())
    act_url = f'{config.SITE_URL}/account/activation?uid={user.id.hex()}&code={act_code}'

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


async def send_password_reset(user):
    act_code = user.reset_key.hex()
    act_url = f'{config.SITE_URL}/account/password_reset?uid={user.id.hex()}&code={act_code}'

    content = f'''重置密码<br/><br/>

    您好，{user.nickname}。<br/>
    您收到这封邮件，是由于在 {config.SITE_NAME} 进行了忘记密码操作。<br/>
    如果您未申请密码重置，请忽略这封电子邮件，您的密码将不作任何更改。<br/>
    <br/><br/>

    点击下面的链接进行密码重置：<br/>
    <a href="{act_url}" target="_blank">{act_url}</a><br/>
    （如果上面不是链接形式，请将该地址手工复制到浏览器地址栏中打开以完成验证）<br/><br/>

    建议您设置易于记住且安全程度较高的密码。尽量不要使用他人容易猜到的密码，而是组合使用大小写字母以及数字和/或特殊字符。<br/>
    此链接将在12小时内有效，12小时后需要重新进行操作。<br/><br/>

    向您问好，<br/>
    {config.SITE_NAME} 管理团队<br/>
    {config.SITE_URL}<br/>
    '''

    return await send(f'{user.nickname} <{user.email}>', f'[{config.SITE_NAME}] 重置密码', content)
