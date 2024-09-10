from common.log_util import log


class ENV:
    # 环境信息：test 测试  prod 准生产 # 从pytest命令行获取
    info = None


# 测试环境服务域名配置
class UrlTestConfig:
    api_backend = "http://api_backend.cn:8899"


# 准生产环境服务域名配置
class UrlProdConfig:
    api_backend = "http://api_backend.cn:8899"


def get_url(server_name):
    if ENV.info == "test":
        url = getattr(UrlTestConfig, server_name)
        log.info(f"测试环境获取服务域名 - {server_name} : {url}")
    elif ENV.info == "prod":
        url = getattr(UrlProdConfig, server_name)
        log.info(f"准生产环境获取服务域名 - {server_name} : {url}")
    else:
        raise Exception("--env 环境信息有误")
    return url
