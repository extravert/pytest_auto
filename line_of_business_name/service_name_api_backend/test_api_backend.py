import pytest
from time import sleep
import allure
from common.data_parser import parser, assert_response
from config.mysql import get_mysql_conn
from common.log_util import log
from common.faker_util import get_name, get_id_card, get_phone_number
from config.redis import get_redis_conn
from common.yaml_util import yaml_load
import os
from common.request_util import send_request
from common.global_util import g


# 加入yaml用例支持，可选择字典维护用例，也可用yaml维护用例
# from line_of_business_name.service_name_api_backend.data import api_backend
api_backend = yaml_load(os.path.join(os.path.dirname(__file__), 'data.yaml'))
# api_backend = yaml_load(os.path.join(os.getcwd(), 'line_of_business_name', 'service_name_api_backend', 'data.yaml'))

# 简化测试用例 下面的测试用例公共部分抽取出来 看上去更简洁
def simplify_code(data_dict, parameter):
    sleep(1)
    allure.dynamic.story(data_dict["story"])
    allure.dynamic.title(parameter["title"])
    request_body = parser("api_backend", data_dict, parameter["data"])
    response = send_request(request_body)
    assert_response(response, parameter["assert"])


@allure.feature("flask后端接口测试")
class TestApiBackend:

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

    @allure.story("测试故事1")
    @pytest.mark.xfail(reason='预期失败用例')
    @pytest.mark.parametrize("param", [{"title": "标题1", "param": 2, "assert": 3}])
    def test_case_one(self, param):
        sleep(1)
        allure.dynamic.description("测试故事1-描述信息")
        allure.dynamic.severity(allure.severity_level.CRITICAL)  # 用例级别严重
        # allure动态标题
        allure.dynamic.title(param["title"])
        log.info("测试faker数据")
        log.info(f"{get_name()}  {get_phone_number()}  {get_id_card()}")
        # pytest.assume(False) # 多重断言插件，断言失败继续执行下面
        assert param["param"] + 2 == param["assert"]

    @pytest.mark.multiprocess  # 此用例分组到可多进程跑测
    @pytest.mark.parametrize("parameter", api_backend["get_student"]["parameter_list"])
    def test_get_student(self, parameter, fixture_get_token):
        data_dict = api_backend["get_student"]
        data_dict["headers"]["Cookie"] = fixture_get_token
        simplify_code(data_dict, parameter)

    @pytest.mark.multiprocess  # 此用例分组到可多进程跑测
    @pytest.mark.parametrize("parameter", api_backend["post_student"]["parameter_list"])
    def test_post_student(self, parameter):
        data_dict = api_backend["post_student"]
        simplify_code(data_dict, parameter)

    @pytest.mark.multiprocess  # 此用例分组到可多进程跑测
    @pytest.mark.parametrize("parameter", api_backend["put_student"]["parameter_list"])
    def test_put_student(self, parameter):
        data_dict = api_backend["put_student"]
        simplify_code(data_dict, parameter)

    @pytest.mark.multiprocess  # 此用例分组到可多进程跑测
    @pytest.mark.parametrize("parameter", api_backend["delete_student"]["parameter_list"])
    def test_delete_student(self, parameter):
        data_dict = api_backend["delete_student"]
        log.info(g.test)  # 测试全局变量
        simplify_code(data_dict, parameter)
