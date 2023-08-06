# /usr/bin/python
# coding=utf-8

"""
auth:wuqichao@playcrab.com
date:2014-06-17 12:00
"""

import commands


class load_used:

    def __init__(self):
        pass

    def run(self):

        cmd = """uptime|awk '{print $NF}'"""
        (status, output) = commands.getstatusoutput(cmd)

        if status == 0:
            return {'flag': 1, 'result': output.split(), 'mod': self.__class__.__name__}
        else:
            return {'flag': 0, 'result': output, 'mod': self.__class__.__name__}
