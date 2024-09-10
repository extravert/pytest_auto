from config.env import get_url
import jsonpath
from common.log_util import log


def update_data(data, parameter_data):
    #  如果通用参数为字典，参数化参数也为字典，使用参数化参数更新通用参数  ex: {"xx": "xx"}
    if isinstance(data, dict) and isinstance(parameter_data, dict):
        data.update(parameter_data)  # 用于将一个字典的键/值对更新到另一个字典中 更新为parameter_data中的值
    else:
        # 如果通用参数是字符串、列表(元素为字符、数字、字典)，直接使用参数化参数据替换通用参数 ex: ["xx", "xx"]
        data = parameter_data
    return data

# 解析请求数据 并返回请求体
def parser(server_name, data_dict: dict, parameter_data=None):
    """
    :param server_name: env.py 中的服务域名 类型str  ex: api_backend
    :param data_dict: test_xxx.py测试用例对应data.py中的接口请求数据字典  ex: api_backend["get_student"]
    :param parameter_data: data.py 参数化列表中一项中的data ex: api_backend["get_student"]["parameter_list"][0]["data"]
    :return: 返回请求数据 dict
    """
    # 获取配置中的服务器域名，拼接path
    url = get_url(server_name) + data_dict.get("path", "")
    method = data_dict.get("method", "get")
    headers = data_dict.get("headers", {})
    params = data_dict.get("params", {})
    data = data_dict.get("data", {})
    json = data_dict.get("json", {})

    #  参数化参数不为空，则用参数化参数去更新或者替换通用参数
    if parameter_data:
        # params、data、json 理论上三种传参格式互斥，只可一个不为空，特殊场景后续扩展
        if params:
            params = update_data(params, parameter_data)
        if data:
            data = update_data(data, parameter_data)
        if json:
            json = update_data(json, parameter_data)

    request_body = {
        "url": url,
        "method": method,
        "headers": headers,
        "params": params,
        "data": data,
        "json": json
    }

    return request_body


def assert_response(response_dict, expect_dict):
    """
    :param response_dict: request请求返回的结果字典，类型 dict
    :param expect_dict: 预期结果字典， 类型 dict
    """
    if isinstance(response_dict, dict):
        log.info(f"\n----------   assertion  ----------\n"
                 f"预期结果: {expect_dict}\n"
                 f"实际结果: {response_dict}")
        # 遍历预期结果的key，使用jsonpath获取请求结果的value，与预期结果value比对
        for k in expect_dict.keys():
            res_list = jsonpath.jsonpath(response_dict, '$..' + str(k))  # 返回列表
            assert expect_dict[k] in res_list
    else:
        log.warning("请求结果不为dict字典类型，跳过断言!")
