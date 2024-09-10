import pytest
from time import sleep
import allure
from common.data_parser import parser, assert_response
from config.mysql import get_mysql_conn
from common.log_util import log
from config.redis import get_redis_conn
from common.yaml_util import yaml_load
import os
from common.request_util import send_request
from common.global_util import g

api_backend = yaml_load(os.path.join(os.path.dirname(__file__), 'data.yaml'))


# log.info(api_backend)
# 其他信息都是pytest框架输出的收集测试用例信息

@allure.feature("flask后端接口测试")
class TestApiBackend:

    # 先执行 下面的 exec函数 然后执行 test_XXX函数 然后执行setup_class
    @classmethod
    def setup_class(cls):
        # 获取数据库连接，执行sql测试
        log.info("setup_class")
        # 数据库连接根据db库名单例，相同库返回同一个连接
        conn = get_mysql_conn("api_auto")
        conn1 = get_mysql_conn("api_auto")
        # conn.execute_dml("insert into test_xdist(msg) values ('%s')" % "class_setup-数据库写入测试")
        conn.execute_dml("insert into test_xdist(msg) values (%s)", "class_setup-数据库写入测试")
        conn1.fetchone("select * from test_xdist limit %s", 1)
        g.test = "test yeah"  # 测试设置全局变量

    @classmethod
    def teardown_class(cls):
        log.info("steup_teardowm")
        # 获取redis连接，执行命令测试
        # redis连接根据host单例，相同host返回同一个连接
        rs = get_redis_conn("api_backend")
        rs1 = get_redis_conn("api_backend")
        rs.set("name", "xp")
        rs1.get("name")

    # 如果所有的用例，均是如下结构
    # 不做数据校验，没有上下用例关联，只有公共的session前置，那可继续进行如下简化
    case_str = ""
    for api in api_backend:
        # 多线程测试用例
        case_str += f"""\n@pytest.mark.multiprocess
@pytest.mark.parametrize("parameter", api_backend["{api}"]["parameter_list"])
def test_{api}(self, parameter, fixture_get_token):
    log.info(g.test)
    data_dict = api_backend["{api}"]
    data_dict["headers"]["Cookie"] = fixture_get_token
    sleep(1)
    allure.dynamic.story(data_dict["story"])
    allure.dynamic.title(parameter["title"])
    request_body = parser("api_backend", data_dict, parameter["data"])
    response = send_request(request_body)
    assert_response(response, parameter["assert"])
    """
    print(case_str)
    exec(case_str)
