#!/usr/bin/env python
# encoding: utf-8


"""
mail:wqc2008@gmail.com
@createtime: 17/9/1 上午11:02
@license: Apache Licence 2.0
usege:
    ......
    
"""

import json
import socket
import base64
import argparse


from DoraClient.tools.config import read_config
from DoraClient.tools.client import Monitor

if __name__ == "__main__":

    host = "127.0.0.1"
    port = 9876

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ini",action="store", help="ini filename")
    args = parser.parse_args()

    if args.ini:
        host = read_config(args.ini, 'tcpserver','host')
        port = read_config(args.ini, 'tcpserver', 'port')

        data = Monitor()

        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.connect((host,port))
        client.send(base64.b64encode(json.dumps(data))+'\n')
        client.close()

