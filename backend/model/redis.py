import config
import redis as lib_redis

redis = lib_redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)
