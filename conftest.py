import pytest
from common.log_util import log
from filelock import FileLock
import json
from config.env import ENV
import os
import allure


# 自定义环境信息pytest命令行
def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="test",
        help="set pytest running environment  ex: --env=test  --env=prod"
    )


# 从pytest命令行获取环境信息
@pytest.fixture(scope="session")
def get_env(request):
    ENV.info = request.config.getoption("--env")
    log.info("运行环境: " + ENV.info)
    return ENV.info


# 终结函数，最后执行
@pytest.fixture(scope="session", autouse=True)
def fixture_case_end(request):
    def case_end():
        log.info("测试结束")
    request.addfinalizer(case_end)


# 定义的fixture会在整个测试会话开始时执行一次，并且会在所有的测试用例之前自动执行 这个取决于其中的参数
@pytest.fixture(scope="session", autouse=True)
# fixture 嵌套先执行获取环境信息get_env
# 加入 tmp_path_factory worker_id 用于多进程执行
def fixture_get_token(get_env, tmp_path_factory, worker_id):
    # 单进程执行
    if worker_id == "master":
        # 获取token
        token = {"token": "xpcs"}
        log.info("fixture_get_token master获取token %s" % token['token'])
    else:
        # 多进程执行
        root_tmp_dir = tmp_path_factory.getbasetemp().parent
        fn = root_tmp_dir / "data.json"
        # 这里with里面的语句，理解为是被加锁的，同一时间只能有一个进程访问
        with FileLock(str(fn) + ".lock"):
            if fn.is_file():
                #  session_fixture 获取token已执行，直接从文件中读取token
                token = json.loads(fn.read_text())
                log.info("fixture_get_token slave使用token %s" % token['token'])
            else:
                token = {"token": "xpcs"}
                fn.write_text(json.dumps(token))
                log.info("fixture_get_token slave获取token %s" % token['token'])

    yield token['token']
    # session 结束后自动执行如下
    log.info("session结束")


# 用例失败自动执行钩子函数
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    # 获取钩子方法的调用结果
    outcome = yield
    rep = outcome.get_result()
    # 仅仅获取用例call 执行结果是失败的情况, 不包含 setup/teardown
    if rep.when == "call" and rep.failed:
        mode = "a" if os.path.exists("failures") else "w"
        with open("failures", mode) as f:
            # let's also access a fixture for the fun of it
            if "tmpdir" in item.fixturenames:
                extra = " (%s)" % item.funcargs["tmpdir"]
            else:
                extra = ""
            f.write(rep.nodeid + extra + "\n")

        with allure.step("用例运行失败，可加入信息"):
            allure.attach("失败内容: ----xpcs----", "失败标题", allure.attachment_type.TEXT)
