import app
import locale
from wtforms import Form
from model.redis import redis
from slim.base.view import BaseView
from typing import Union
from slim.retcode import RETCODE
from ipaddress import IPv4Address, IPv6Address

route = app.app.route


class ValidateForm(Form):
    class Meta:
        locales = [locale.getdefaultlocale()[0]]


async def get_fuzz_ip(view) -> str:
    ip = await view.get_ip()

    # 数据脱敏，将IP地址最后一位填充为 0
    if isinstance(ip, IPv4Address):
        return str(ip).rsplit('.', 1)[0] + '.0'
    elif isinstance(ip, IPv6Address):
        return str(ip).rsplit(':', 1)[0] + ':0'
    else:
        raise ValueError("unexpected ip address: %s", ip)


async def get_ip(view: BaseView) -> bytes:
    return (await view.get_ip()).packed


async def same_user(view: BaseView) -> Union[bytes, None]:
    if view.current_user:
        return view.current_user.id.tobytes()

    view.finish(RETCODE.PERMISSION_DENIED)


def cooldown(interval, redis_key_template, *, unique_id_func=get_ip, cd_if_unsuccessed=None):
    def wrapper(func):
        async def myfunc(self: BaseView, *args, **kwargs):
            # 有可能在刚进入的时候，上一轮已经finish了，那么直接退出
            if self.is_finished: return

            unique_id = await unique_id_func(self)
            if self.is_finished: return

            if unique_id is None:
                return await func(self, *args, **kwargs)

            key = redis_key_template % unique_id
            if await redis.get(key):
                self.finish(RETCODE.TOO_FREQUENT, await redis.ttl(key))
            else:
                ret = await func(self, *args, **kwargs)
                # 如果设定了失败返回值CD （请求完成同时未成功）
                if self.is_finished and cd_if_unsuccessed is not None:
                    if self.ret_val['code'] != RETCODE.SUCCESS:
                        await redis.set(key, '1', expire=cd_if_unsuccessed)
                        return ret

                # 如果没有，检查是否存在豁免值
                if not getattr(self, 'cancel_cooldown', None):
                    return ret

                # 所有跳过条件都不存在，设置正常的expire并退出
                await redis.set(key, '1', expire=interval)
                return ret
        return myfunc
    return wrapper
