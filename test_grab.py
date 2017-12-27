# -*- coding: utf-8 -*-
from grab import Grab
from pyquery import PyQuery as pq
import re
import logging
logging.basicConfig(level=logging.DEBUG)

NEWS_COUNT = 10
def loadPage(url):
    g = Grab()
    g.setup(log_dir='grab')
    g.setup(timeout = 15, connect_timeout = 100)
    #g.setup(proxy='186.170.31.134:8080', proxy_type='http')

    # g.proxylist.set_source('file', 'include/proxy.txt')

    # g.proxylist.set_source('file', location='include/proxy.txt')
    # g.proxylist.proxy_list

    g.go(url)
    response = str(g.response.body)
    return response



ss = loadPage('https://f.ua/articles/104/');
a = ss.decode('cp1251')
str = 'внимание'
print a.find(str.encode('cp1251'))