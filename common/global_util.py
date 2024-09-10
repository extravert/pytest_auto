from common.log_util import log


class G:
    def __init__(self):
        # self.storage = {}  # getattr会反复递归，通过将变量存入object类解决
        # 在 G 类的实例中创建一个名为 storage 的属性，并将其初始化为一个空字典。
        # object类是不可变的，self指的是实例本身
        object.__setattr__(self, "storage", {})

    def __setattr__(self, key, value):
        log.info(f"设置全局变量: {key}={value}")
        self.storage[key] = value

    def __getattr__(self, item):
        value = self.storage.get(item, None)
        log.info(f"获取全局变量: {item}={value}")
        return value


g = G()

if __name__ == '__main__':
    # 用例中引入g,  g.x=10 设置， g.x获取即可
    g.x = 10
    g.b = 0
    print(g.x)
    print(g.b)
