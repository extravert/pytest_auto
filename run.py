import pytest
import os


# 用例调试入口
if __name__ == '__main__':
    # 设置测试文件路径，-n 3表示并发数为3，--cache-clear表示清除缓存，--env=prod表示指定环境
    pytest.main([r"line_of_business_name\\service_name_api_backend\\test_api_backend_bak.py", "-n 3", "--cache-clear", "--env=prod"])
    # pytest.main([r"-m multiprocess", "-n 3", "--cache-clear", "--env=prod"])
    os.system(r"allure generate allure_result -c -o allure_report")
    os.system(r"allure open -h 127.0.0.1 -p 8899 allure_report")
