#!/usr/bin/python
# coding=utf-8


import os, logging
import os.path
from threading import Thread
from DoraClient.tools.logged import logged

__ALL__=["AutoLoad","Child","Monitor"]


class AutoLoad(object):
    """
    自动引入模块类
    """

    def __init__(self, class_path):

        self.class_path = class_path

    def import_and_get_mod(self, string, parent_mod=None):
        """
        动态引入模块
        """
        mods = string.split('.')
        child_mod_str = '.'.join(mods[1:])
        if parent_mod is None:
            if len(mods) > 1:

                return self.import_and_get_mod(child_mod_str, __import__(string))
            else:
                return __import__(string)
        else:
            mod = getattr(parent_mod, mods[0])
            if len(mods) > 1:
                return self.import_and_get_mod(child_mod_str, mod)
            else:
                return mod

    def get_mod(self):
        """
        动态实例化工厂类
        """
        if self.class_path:
            # 组装引入字符串
            name = self.class_path
            # 引入modle
            return self.import_and_get_mod(name)


class Child(Thread):

    def __init__(self, filename):
        Thread.__init__(self)
        self.filename = filename
        self.res = None

    def run(self):
        filename = self.filename.split('.')[0]
        a = AutoLoad('DoraClient.custom.%s' % filename)
        m = a.get_mod()

        obj = getattr(m, '%s' % filename)()
        self.res = obj.run()

    def get_result(self):
        return self.res

@logged(logging.DEBUG)
def Monitor():

    result = []

    # 当前文件的路径
    pwd = os.getcwd()
    # 当前文件的父路径
    root_dir = os.path.abspath(os.path.dirname(pwd) + os.path.sep + "./custom")
    # 为了方便扩展而不改client代码，直接加载custom包中的代码模块
    for parent, dirs, files in os.walk(root_dir):

        for filename in files:

            if filename == '__init__.py':
                continue

            if filename.endswith('.py'):
                t = Child(filename)
                result.append(t)

    # 启动进程监控各项值标
    for res in result:
        res.start()

    # 等待结果，并收集执行结果
    for res in result:
        res.join()

    data = []
    for res in result:
        data.append(res.get_result())

    return data


# if __name__ == '__main__':
#     clint()
