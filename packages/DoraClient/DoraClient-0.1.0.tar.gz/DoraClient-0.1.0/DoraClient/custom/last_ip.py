# /usr/bin/python
# coding=utf-8

"""
auth:wuqichao@playcrab.com
date:2014-06-17 12:00
"""

import commands


class last_ip:

    def __init__(self):
        pass

    def run(self):

        cmd = """last -n 10 | awk '{print $3}'|grep '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}'"""
        (status, output) = commands.getstatusoutput(cmd)

        if status == 0:
            return {'flag': 1, 'result': output.split(), 'mod': self.__class__.__name__, 'is_multi': 1}
        else:
            return {'flag': 0, 'result': output, 'mod': self.__class__.__name__}
