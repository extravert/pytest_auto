from common.mysql_util import MySql
from config.env import ENV
from common.log_util import log


# 数据库连接配置
class MysqlTestConfig:
    """Mysql测试环境配置"""
    api_auto = {'host': 'localhost',
                'port': 3306,
                'db': 'api_auto',
                'user': 'root',
                'password': '123456',
                'autocommit': True
                }


class MysqlProdConfig:
    """Mysql准生产环境配置"""
    api_auto = {'host': 'localhost',
                'port': 3306,
                'db': 'api_auto',
                'user': 'root',
                'password': '123456',
                'autocommit': True
                }


def get_mysql_conn(db_name):
    if ENV.info == "test":
        log.info("测试环境建立mysql连接 - " + db_name)
        return MySql(getattr(MysqlTestConfig, db_name))
    elif ENV.info == "prod":
        log.info("准生产环境建立mysql连接 - " + db_name)
        return MySql(getattr(MysqlProdConfig, db_name))
    else:
        raise Exception("--env 环境信息有误")


if __name__ == '__main__':
    ENV.info = "test"
    conn = get_mysql_conn("api_auto")
    t = [5980, 5981, 5982]
    t1 = (5980, 5981)
    res = conn.fetchone("select * from test_xdist where id = %s", 5982)
    print(res)
    res = conn.fetchall("select * from test_xdist where id in %s", t)
    print(res)
    res = conn.fetchall("select * from test_xdist where id in %s", t1)
    print(res)
