#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/14 15:01
# @Author  : David Deng
# @File    : zhihu_login_requests.py

import requests

try:
    import cookielib

except:
    import http.cookiejar as cookielib

import re


def zhihu_login(account,password):
    #知乎登录

   if re.match("^1\d{10}",account):
       print "手机号码登录"
       post_url = 'https://www.zhihu.com/api/v3/oauth/sign_in'
       post_data = {
           "client_id":"c3cef7c66a1843f8b3a9e6a1e3160e20",
           "grant_type":"password",
           "lang":"cn",
           "password":"19861123wei",
           "ref_source":"homepage",
           "source":"com.zhihu.web",
           "username":"+8615521050893",
           "utm_source":"",
           "signature":"3f6dece855de8984a3a566097ac0f33fa1f69d8b"
       }

       result = requests.post(post_url,data=post_data)

       print result.text


def main():

    zhihu_login("15521050893","19861123wei")

if __name__ == '__main__':
    main()

