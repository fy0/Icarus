from slim.retcode import RETCODE

import app
import locale
from wtforms import Form
from model.redis import redis
from slim.base.view import BaseView

route = app.app.route


class ValidateForm(Form):
    class Meta:
        locales = [locale.getdefaultlocale()[0]]


async def get_ip(view) -> bytes:
    ip_addr = view._request.transport.get_extra_info('peername')[0]
    return ip_addr.encode('utf-8')


def cooldown(interval, redis_key_template, *, unique_id_func=get_ip):
    def wrapper(func):
        async def myfunc(self: BaseView):
            unique_id = await unique_id_func(self)
            key = redis_key_template % unique_id
            if await redis.get(key):
                self.finish(RETCODE.TOO_FREQUENT, await redis.ttl(key))
            else:
                await redis.set(key, '1', expire=interval)
                return await func(self)
        return myfunc
    return wrapper
