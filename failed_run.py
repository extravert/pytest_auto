import pytest
import os


# 失败用例重跑
if __name__ == '__main__':
    pytest.main([r"line_of_business_name", "--lf", "--clean-alluredir", "--alluredir=allure_result",  "--env=prod"])
    os.system(r"allure generate allure_result -c -o allure_report")
    os.system(r"allure open -h 127.0.0.1 -p 8899 allure_report")

