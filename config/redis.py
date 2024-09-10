from common.redis_util import Redis
from config.env import ENV
from common.log_util import log


class RedisTestConfig:
    api_backend = {'host': 'api_backend.cn', 'password': 'redis123',
                   'port': 6379, 'db': 0, 'decode_responses': True}


class RedisProdConfig:
    api_backend = {'host': 'api_backend.cn', 'password': 'redis123',
                   'port': 6379, 'db': 0, 'decode_responses': True}


def get_redis_conn(name):
    if ENV.info == "test":
        log.info("测试环境建立redis连接 - " + name)
        return Redis(getattr(RedisTestConfig, name))
    elif ENV.info == "prod":
        log.info("准生产环境建立redis连接 - " + name)
        return Redis(getattr(RedisProdConfig, name))
    else:
        raise Exception("--env 环境信息有误")
