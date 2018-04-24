#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/11 16:31
# @Author  : David Deng
# @File    : main.py

'''
用于调试，生产环境不需要
'''

from scrapy.cmdline import execute
import  sys,os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

execute(['scrapy','crawl','jobbole'])

