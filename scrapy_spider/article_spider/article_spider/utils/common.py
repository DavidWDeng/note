#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/12 14:41
# @Author  : David Deng
# @File    : common.py

import hashlib
import re

def get_md5(url):
    if isinstance(url,str): #python3需要进行处理，Python2不用
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()



if __name__ == "__main__":
    print get_md5("http://www.163.com")