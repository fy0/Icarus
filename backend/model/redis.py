import config
import aioredis
from lib.ref import Reference

redis: aioredis.Redis = Reference()


async def init(loop):
    from model.topic import Topic
    address = 'redis://%s:%d' % (config.REDIS_HOST, config.REDIS_PORT)
    redis._obj = await aioredis.create_redis(address, loop=loop, timeout=30)
    await Topic.weight_redis_init()

# user

RK_USER_ACTCODE_BY_USER_ID = b'ic_user_actcode_by_user_id_%b'
RK_USER_RESET_KEY_BY_USER_ID = b'ic_user_reset_key_by_user_id_%b'

RK_USER_LAST_REQUEST_ACTCODE_BY_USER_ID = b'ic_user_last_request_actcode_by_user_id_%b'
RK_USER_LAST_REQUEST_RESET_KEY_BY_USER_ID = b'ic_user_last_request_reset_key_by_user_id_%b'

# topic

RK_TOPIC_WEIGHT_MAX = b'ic_topic_weight_max'
