#!/usr/bin/env python
# encoding: utf-8


"""
mail:wqc2008@gmail.com
@createtime: 17/8/30 下午5:55
@license: Apache Licence 2.0
usege:
    ......
    
"""


from DoraClient.tools.update import AutoUpdate

if __name__ == "__main__":

    a = AutoUpdate("ldap")
    a.upgrade_if_needed()
