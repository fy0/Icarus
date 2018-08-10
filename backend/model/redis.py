import config
import redis as lib_redis

redis = lib_redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)

RK_USER_ACTCODE_BY_USER_ID = b'ic_user_actcode_by_user_id_%b'
RK_USER_RESET_KEY_BY_USER_ID = b'ic_user_reset_key_by_user_id_%b'
