import logging
import os

# create logger
log = logging.getLogger("pytest_api_auto")
log.setLevel(logging.INFO)

# create file handler
# mode 默认为a追加模式，如果修改为w为覆盖模式，多进程运行会出现日志缺失和错乱
# 获取项目根目录拼接  #  如果使用相对路径 ../pytest.log 执行根目录main函数运行，日志就打到项目外了
fh = logging.FileHandler(os.path.join(os.path.dirname(os.path.dirname(__file__)), "pytest.log"),
                         mode='a', encoding='UTF-8')
fh.setLevel(logging.INFO)

# create stream handler
sh = logging.StreamHandler(stream=None)

# create formatter
fmt = "%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s"
formatter = logging.Formatter(fmt)

# add handler and formatter to logger
fh.setFormatter(formatter)
sh.setFormatter(formatter)

log.addHandler(fh)
log.addHandler(sh)


if __name__ == '__main__':
    log.info("啊啊")
    log.warning("warning")
    # print(os.path.join(os.path.dirname(os.path.dirname(__file__)), "pytest.log"))
