# /usr/bin/python
# coding=utf-8

"""
auth:wuqichao@playcrab.com
date:2014-06-17 12:00
"""

import commands


class df_used:
    def __init__(self):
        pass

    def run(self):

        cmd = """df -B 1M | grep '/dev' | awk '{print $2" "$3}'|awk 'BEGIN{s1=0;s2=0}{s1+=$1;s2+=$2}END{printf "%.2f",(s2/s1)*100}'"""
        (status, output) = commands.getstatusoutput(cmd)

        if status == 0:
            return {'flag': 1, 'result': output.split(), 'mod': self.__class__.__name__}
        else:
            return {'flag': 0, 'result': output, 'mod': self.__class__.__name__}
