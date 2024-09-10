import requests
from common.log_util import log


def send_request(request_body, **kwargs):
    """
    :param request_body 请求数据
    :param kwargs: 扩展支持 files 上传文件、proxy 代理等
    :return:
    """
    url = request_body["url"]
    method = request_body["method"]
    headers = request_body["headers"]
    params = request_body["params"]
    data = request_body["data"]
    json = request_body["json"]

    if not url.startswith("http://") and not url.startswith("https://"):
        raise ValueError("请求url缺少协议名")
    if method.lower() not in ("get", "post", "put", "delete"):
        raise ValueError(f"暂不支持请求方法 - {method} - 可后续扩展")

    data_log = ""
    if params:
        data_log = f"params: {params}"
    if data:
        data_log = f"data: {data}"
    if json:
        data_log = f"json: {json}"
    if kwargs:
        data_log += f"\nkwargs: {kwargs}"

    log.info("\n----------   request  info  ----------\n"
             f"url: {url}\n"
             f"method: {method}\n"
             f"headers: {headers}\n"
             f"{data_log}"
             )

    try:
        response = requests.request(**request_body, timeout=30, **kwargs)
    except Exception as e:
        log.warning(f"请求发生异常!!!")
        raise Exception(f"request exception {str(e)}")

    if response.status_code == 200:
        log.info("\n----------   response  info  ----------\n"
                 f"status: {response.status_code}\n"
                 f"headers: {response.headers}\n"
                 f"body: {response.text}")
    else:
        log.warning(f"请求失败!!! 返回码不为200, 状态码为: {response.status_code}")
        log.warning("\n----------   response  info  ----------\n"
                    f"text: {response.text}\n"
                    f"raw: {response.raw}")
        raise ValueError("返回码不为200")
    try:
        # 返回为字典类型
        return response.json()
    except requests.exceptions.JSONDecodeError:
        log.warning("响应参数不为json，返回响应 response对象")
        return response


if __name__ == '__main__':
    pass
    # data = {"name": "xpcs"}
    # headers = {"cookie": "xpcs"}
    # resp = send_request("http://api_backend.cn:8899/student", "get", data, headers)
    # assert resp["code"] == 0
    #
    # data = {"name": "xpcs"}
    # headers = {"cookie": "xpcs", "Content-Type": "application/x-www-form-urlencoded"}
    # resp = send_request("http://api_backend.cn:8899/student", "post", data, headers)
    # assert resp["code"] == 0
    #
    # data = {"name": "xpcs"}
    # headers = {"cookie": "xpcs", "Content-Type": "application/json"}
    # resp = send_request("http://api_backend.cn:8899/student", "post", data, headers)
    # assert resp["code"] == 0
    #
    # data = "一段文本"
    # headers = {"cookie": "xpcs", "Content-Type": "application/json"}
    # resp = send_request("http://api_backend.cn:8899/student", "post", data, headers)
    # assert resp["code"] == 0
