# 传参不破坏原始request，所以如果想用params传参则写params
# 如果想data传参，则写data，如果想json传参则写json
# 三者理论上是互斥的，就是指选其中一种

api_backend = {
    "get_student": dict(path="/student",
                        method="get",
                        # headers 不包含Content-Type 则request使用params传参
                        headers={},
                        # 通用参数，每次请求使用
                        params={"test": "test"},
                        #  参数化参数，每次使用其中一项，更新通用参数
                        parameter_list=[
                            {"title": "获取学生信息-张三", "data": {"name": "张三"}, "assert": {"code": 0, "msg": "ok"}},
                            {"title": "获取学生信息-李四", "data": {"name": "李四"}, "assert": {"code": 0, "msg": "ok"}},
                            {"title": "获取学生信息-王五", "data": {"name": "王五"}, "assert": {"code": 0, "msg": "ok"}}
                        ]),
    'post_student': dict(path="/student",
                         method="post",
                         headers={"Cookie": "", "Content-Type": "application/x-www-form-urlencoded"},
                         data={"test": "test"},
                         parameter_list=[
                             {"title": "新增学生信息-张三", "data": {"name": "张三"}, "assert": {"code": 1, "msg": "ok"}},
                             {"title": "新增学生信息-李四", "data": {"name": "李四"}, "assert": {"code": 0, "msg": "ok"}},
                             {"title": "新增学生信息-王五", "data": {"name": "王五"}, "assert": {"code": 0, "msg": "ok"}}
                         ]),
    'put_student': dict(path="/student",
                        method="put",
                        headers={"Cookie": "", "Content-Type": "application/json"},
                        json={"test": "test"},
                        parameter_list=[
                            {"title": "更新学生信息-张三", "data": {"name": "张三"}, "assert": {"code": 0, "msg": "ok"}},
                            {"title": "更新学生信息-李四", "data": {"name": "李四"}, "assert": {"code": 0, "msg": "okk"}},
                            {"title": "更新学生信息-王五", "data": {"name": "王五"}, "assert": {"code": 0, "msg": "ok"}}
                        ])
}
