import redis
from common.log_util import log
from functools import wraps


# 装饰器，同一个redis只建立一次连接
def decorate_single(cls):
    connect_list = {}

    @wraps(cls)  # 装饰后不改变 __name__
    def wrapper(*args, **kwargs):
        nonlocal connect_list
        host = args[0]["host"]
        if host not in connect_list:
            connect_list[host] = cls(*args, **kwargs)
            log.info(f"建立redis连接并返回 - {host}")
        else:
            log.info(f"redis连接已建立，直接返回 - {host}")
        return connect_list[host]
    return wrapper


@decorate_single
class Redis:

    def __init__(self, db_config):
        """
        :params: db_config 数据库配置 类型为字典
        """
        self.pool = redis.ConnectionPool(**db_config)
        self.rs = redis.Redis(connection_pool=self.pool)

    def del_key(self, key):
        """
        :param key: redis key str字符类型
        :return: 删除成功返回 True 否则 False
        """
        log.info(f"redis 删除key {key}")
        if self.rs.delete(key) == 1:
            log.info(f"key {key} 删除成功")
            return True
        else:
            log.warning(f"key: {key} 不存在!")
            return False

    def del_keys(self, keys_pattern):
        """
        :param keys_pattern: key通配符 str字符类型 ex: *name*
        :return:删除成功返回 True 否则 False
        """
        log.info(f"redis 删除keys 通配符 {keys_pattern}")
        keys = self.rs.keys(keys_pattern)
        if keys:
            log.info(f"redis 删除keys {keys}")
            for k in keys:
                self.rs.delete(k)
            log.info(f"keys {keys} 删除成功")
            return True
        else:
            log.warning("通配符未匹配到key!")
            return False

    def set(self, key, value, ex=8 * 60 * 60):
        """
        操作str类型
        :param key: redis key str字符类型
        :param value: str字符类型
        :param ex: 数据超时时间，默认8小时
        return: 写入成功返回 True
        """
        log.info(f"redis str类型 数据写入 key: {key}  value: {value}")
        return self.rs.set(key, value, ex=ex)

    def get(self, key):
        """
        操作str类型
        :param key: redis key str字符类型
        :return: 获取到返回str字符类型 # 未获取到返回 None
        """
        data = self.rs.get(key)
        log.info(f"redis str类型 数据获取 key: {key}  value: {data}")
        return data

    def lrange(self, key):
        """
        操作list类型
        :param key: redis key str字符类型
        return: 获取到返回list列表类型 # 未获取到返回空列表 []
        """
        data = self.rs.lrange(key, 0, -1)
        log.info(f"redis list类型 数据获取 key: {key}  values: {data}")
        return data

    def smembers(self, key):
        """
        操作 set 集合
        :param key: redis key str字符类型
        return: 获取到返回set集合类型 # 未获取到返回空集合 set()
        """
        data = self.rs.smembers(key)
        log.info(f"redis set类型 数据获取 key: {key}  values: {data}")
        return data

    def zrange(self, key):
        """
        操作 zset 有序集合
        :param key: redis key str字符类型
        return: 获取到返回list列表类型 # 未获取到返回空列表 []
        """
        data = self.rs.zrange(key, 0, -1)
        log.info(f"redis zset类型 数据获取 key: {key}  values: {data}")
        return data

    # hash 操作 hset hget 后续可扩展

    def close(self):
        """
        function:关闭数据库连接
        params: rs Redis对象
        """
        self.rs.close()
