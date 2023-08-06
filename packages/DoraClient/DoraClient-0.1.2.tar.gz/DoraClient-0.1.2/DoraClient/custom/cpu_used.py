# /usr/bin/python
# coding=utf-8

"""
auth:wuqichao@playcrab.com
date:2014-06-17 12:00

modify date:2014-08-15 12:20
auth:wuqichao@playcrab.com
modify: 将原来的mpstat中断数改为/proc/stat中cpu的数据
"""

import commands


class cpu_used:
    def __init__(self):
        pass

    def run(self):
        # vmstat
        # cmd = """mpstat -P ALL  1 10 | grep all | awk '{print $11}' | awk 'BEGIN{sum=0;num=0}{sum+=$1;num+=1}END{print sum/num}'"""
        cmd = """sh custom/cpu_used.sh"""
        (status, output) = commands.getstatusoutput(cmd)

        if status == 0:
            return {'flag': 1, 'result': output.split(), 'mod': self.__class__.__name__}
        else:
            return {'flag': 0, 'result': output, 'mod': self.__class__.__name__}
