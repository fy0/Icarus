import time

from slim.utils import to_bin

import config
from aiohttp import web

from app import app
from lib.utils import get_today_start_timestamp
from model.log_manage import MANAGE_OPERATION, ManageLog
from model.notif import NOTIF_TYPE, Notification
from model._post import POST_TYPES, POST_STATE, POST_VISIBLE
from model.log_manage import ManageLog, MANAGE_OPERATION as MOP
from model.redis import RK_USER_ACTIVE_TIME_ZSET, redis, RK_USER_ANON_ACTIVE_TIME_ZSET
from model.user import USER_GROUP
from slim.base.view import BaseView
from slim.retcode import RETCODE
from view import route
from view.user import UserMixin
from view.ws import WSR


@app.timer(10, exit_when=None)
async def user_online():
    for ws in WSR.connections:
        if not ws.closed:
            await ws.send_json(['user.online', len(WSR.count)])


@route('misc')
class TestBaseView(UserMixin, BaseView):
    @classmethod
    def interface(cls):
        cls.use('info', 'GET')
        cls.use('tick', 'GET')

    async def tick(self):
        """
        定时轮询
        :return:
        """
        data = {}
        now = int(time.time())

        if self.current_user:
            user = self.current_user
            # 检查未读信息
            r = Notification.refresh(user.id)
            c = Notification.count(user.id)
            data['notif_count'] = c

            # 更新在线时间
            await redis.zadd(RK_USER_ACTIVE_TIME_ZSET, now, user.id.tobytes())
        else:
            # TODO: 后面再给auid加几个随机数
            auid = self.params.get('auid', None)
            if auid:
                try:
                    auid = config.LONG_ID_GENERATOR(auid)
                    if not await redis.zscore(RK_USER_ANON_ACTIVE_TIME_ZSET, auid.to_bin()):
                        auid = None
                except TypeError:
                    auid = None

            if not auid:
                new_id = config.LONG_ID_GENERATOR()
                await redis.zadd(RK_USER_ANON_ACTIVE_TIME_ZSET, now, new_id.to_bin())
                data['auid'] = new_id.to_hex()
            else:
                await redis.zadd(RK_USER_ANON_ACTIVE_TIME_ZSET, now, auid.to_bin())

        offset = 30
        data['online'] = await redis.zcount(RK_USER_ACTIVE_TIME_ZSET, min=now - offset) + \
                         await redis.zcount(RK_USER_ANON_ACTIVE_TIME_ZSET, min=now - offset)

        self.finish(RETCODE.SUCCESS, data)

    async def info(self):
        """
        一些后端信息，一般是首次打开页面时获得
        :return:
        """
        extra = {
            'midnight_time': get_today_start_timestamp()
        }

        # 每日首次访问奖励
        if self.current_user:
            daily_reward = self.current_user.daily_access_reward()
            if daily_reward:
                extra['daily_reward'] = {
                    'exp': daily_reward
                }

        self.finish(RETCODE.SUCCESS, {
            'extra': extra,

            'POST_TYPES': POST_TYPES.to_dict(),
            'POST_TYPES_TXT': POST_TYPES.txt,
            'POST_STATE': POST_STATE.to_dict(),
            'POST_STATE_TXT': POST_STATE.txt,
            'POST_VISIBLE': POST_VISIBLE.to_dict(),
            'POST_VISIBLE_TXT': POST_VISIBLE.txt,

            'MANAGE_OPERATION': MANAGE_OPERATION.to_dict(),
            'MANAGE_OPERATION_TXT': MANAGE_OPERATION.txt,

            'USER_GROUP': USER_GROUP.to_dict(),
            'USER_GROUP_TXT': USER_GROUP.txt,
            'USER_GROUP_TO_ROLE': USER_GROUP.GROUP_TO_ROLE,

            'NOTIF_TYPE': NOTIF_TYPE.to_dict(),

            'BACKEND_CONFIG': {
                'USER_NICKNAME_MIN': config.USER_NICKNAME_MIN,
                'USER_NICKNAME_MAX': config.USER_NICKNAME_MAX,
                'USER_NICKNAME_CN_FOR_REG_MIN': config.USER_NICKNAME_CN_FOR_REG_MIN,
                'USER_NICKNAME_FOR_REG_MIN': config.USER_NICKNAME_FOR_REG_MIN,
                'USER_NICKNAME_FOR_REG_MAX': config.USER_NICKNAME_FOR_REG_MAX,
                'USER_PASSWORD_MIN': config.USER_PASSWORD_MIN,
                'USER_PASSWORD_MAX': config.USER_PASSWORD_MAX,

                'TOPIC_TITLE_LENGTH_MIN': config.TOPIC_TITLE_LENGTH_MIN,
                'TOPIC_TITLE_LENGTH_MAX': config.TOPIC_TITLE_LENGTH_MAX,
                'TOPIC_CONTENT_LENGTH_MAX': config.TOPIC_CONTENT_LENGTH_MAX,

                'UPLOAD_STATIC_HOST': config.UPLOAD_STATIC_HOST,
                'UPLOAD_QINIU_DEADLINE_OFFSET': config.UPLOAD_QINIU_DEADLINE_OFFSET,
            },

            'NICKNAME_MIN': config.USER_NICKNAME_MIN,
            'NICKNAME_MAX': config.USER_NICKNAME_MAX,
            'NICKNAME_CN_FOR_REG_MIN': config.USER_NICKNAME_CN_FOR_REG_MIN,
            'NICKNAME_FOR_REG_MIN': config.USER_NICKNAME_FOR_REG_MIN,
            'NICKNAME_FOR_REG_MAX': config.USER_NICKNAME_FOR_REG_MAX,
            'PASSWORD_MIN': config.USER_PASSWORD_MIN,
            'PASSWORD_MAX': config.USER_PASSWORD_MAX,

            'TOPIC_TITLE_LENGTH_MIN': config.TOPIC_TITLE_LENGTH_MIN,
            'TOPIC_TITLE_LENGTH_MAX': config.TOPIC_TITLE_LENGTH_MAX,
            'TOPIC_CONTENT_LENGTH_MAX': config.TOPIC_CONTENT_LENGTH_MAX,

            'retcode': RETCODE.to_dict(),
            'retinfo_cn': RETCODE.txt_cn,
        })
