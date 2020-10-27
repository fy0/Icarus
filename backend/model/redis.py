import config
import aioredis
from lib.ref import Reference

redis: aioredis.Redis = Reference()


async def init(loop):
    from model.topic_model import TopicModel
    redis._obj = await aioredis.create_redis(config.REDIS_URI, loop=loop, timeout=30)
    await TopicModel.weight_redis_init()

# user

RK_USER_ACTIVE_TIME_ZSET = b'ic_user_active_time_zset'  # 最近一次活跃时间
RK_USER_ANON_ACTIVE_TIME_ZSET = b'ic_user_anon_active_time_zset'

RK_USER_REG_CODE_AVAILABLE_TIMES_BY_EMAIL = b'ic_user_reg_code_available_times_by_email_%b'
RK_USER_REG_CODE_BY_EMAIL = b'ic_user_reg_code_by_email_%b'
RK_USER_REG_PASSWORD = b'ic_user_reg_password_by_email_%b'

RK_USER_ACTCODE_BY_USER_ID = b'ic_user_actcode_by_user_id_%b'
RK_USER_RESET_KEY_BY_USER_ID = b'ic_user_reset_key_by_user_id_%b'

RK_USER_LAST_REQUEST_RESET_KEY_BY_USER_ID = b'ic_user_last_request_reset_key_by_user_id_%b'

# topic

RK_TOPIC_WEIGHT_MAX = b'ic_topic_weight_max'
