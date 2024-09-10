import pymysql
from time import sleep
from common.log_util import log
from functools import wraps


# 装饰器，同一个mysql数据库只建立一次连接
def decorate_single(cls):
    connect_list = {}

    @wraps(cls)  # 装饰后不改变 __name__
    def wrapper(*args, **kwargs):
        nonlocal connect_list
        db_name = args[0]["db"]
        if db_name not in connect_list:
            connect_list[db_name] = cls(*args, **kwargs)
            log.info(f"建立mysql连接并返回 - {db_name}")
        else:
            log.info(f"mysql连接已建立，直接返回 - {db_name}")
        return connect_list[db_name]
    return wrapper


@decorate_single
class MySql:

    def __init__(self, db_config: dict):
        """
        :params: db_config 数据库配置 类型为字典
        """
        # 数据库配置
        # autocommit: True 选项很关键，如果不设置，新增数据无法查出
        # mysql默认数据引擎是innodb 默认数据隔离级别重复读，如果事务不提交，那么每次查询，查询都是同一块数据快照
        self.conn = None
        while True:
            try:
                self.conn = pymysql.connect(**db_config)
                break
                # 数据库连接，偶尔会连接不上
                # 报错 pymysql.err.OperationalError: (2013, 'Lost connection to MySQL server during query')
                # 解决办法，就是重新连接
            except pymysql.err.OperationalError:
                log.warning("连接失败，可能环境不稳定，重新连接！")
                sleep(1)
            except Exception as e:
                log.warning("获取mysql连接失败！请检查数据库配置或网络连接")
                raise e

    def fetchone(self, sql_str, *args):
        """
        :param sql_str 数据库sql
        :param args 可变参数，替换sql_str中的占位符，可不传
        :return: 返回查询结果的一条记录，类型是字典; 若未查询到，则返回None
        """
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                log.info(f"执行sql: {sql_str}")
                if args:
                    log.info(f"占位符参数: {args}")
                cursor.execute(sql_str, args)
                data = cursor.fetchone()
                log.info(f"sql执行结果: {data}")
                return data
        except Exception as e:
            log.warning("执行sql失败！")
            raise e

    def fetchall(self, sql_str, *args):
        """
        :param sql_str 数据库sql
        :param args 可变参数，替换sql_str中的占位符，可不传
        :return: 返回查询结果的全部记录，类型是列表，列表元素为字典
        """
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                log.info(f"执行sql: {sql_str}")
                if args:
                    log.info(f"占位符参数: {args}")
                cursor.execute(sql_str, args)
                data = cursor.fetchall()
                log.info(f"sql执行结果: {data}")
            return data
        except Exception as e:
            log.warning("执行sql失败！")
            raise e

    def execute_dml(self, sql_str, *args):
        """
        function: 执行insert、update、delete
        :param sql_str 数据库sql
        :param args 可变参数，替换sql_str中的占位符，可不传
        :return: 无返回
        """
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                log.info(f"执行sql: {sql_str}")
                if args:
                    log.info(f"占位符参数: {args}")
                data = cursor.execute(sql_str, args)
                # 提交操作，我们配置连接是自动提交，所以下面提交步骤也可省略
                self.conn.commit()
                log.info(f"sql执行结果: {data}")
        except Exception as e:
            log.warning("执行sql失败！")
            raise e

    def close(self):
        """
        function:关闭数据库连接
        params: conn 数据库连接
        """
        self.conn.close()