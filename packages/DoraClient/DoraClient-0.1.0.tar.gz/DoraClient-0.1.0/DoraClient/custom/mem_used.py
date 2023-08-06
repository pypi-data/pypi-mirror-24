# /usr/bin/python
# coding=utf-8

"""
auth:wuqichao@playcrab.com
date:2014-06-17 12:00

"""

import commands


class mem_used:
    def __init__(self):
        pass

    def run(self):

        cmd = """cat /proc/meminfo | sed -n '1,4p'|awk '{print $2}'|awk 'BEGIN {sum=0;num=0}{if (num==0){sum=$1;num+=1}else{sum-=$1;num+=1}}END{print sum/1024}'"""

        (status, output) = commands.getstatusoutput(cmd)

        if status == 0:
            return {'flag': 1, 'result': output.split(), 'mod': self.__class__.__name__}
        else:
            return {'flag': 0, 'result': output, 'mod': self.__class__.__name__}
