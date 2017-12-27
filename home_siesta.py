# -*- coding: utf-8 -*-
from grab import Grab
from urllib import urlencode

def loadPage(url,i):
    g = Grab()
    g.setup(log_dir='grab')
    g.setup(timeout = 150, connect_timeout = 100)
    #g.setup(proxy='186.170.31.134:8080', proxy_type='http')
    qs = urlencode({'samo_action':'PRICES',
    'TOWNFROMINC':'25',
    'STATEINC':'26',
    'TOURINC':'706',
    'PROGRAMGROUPINC':'0',
    'PROGRAMINC':'0',
    'CHECKIN_BEG':'20160721',
    'NIGHTS_FROM':'7',
    'CHECKIN_END':'20160722',
    'NIGHTS_TILL':'7',
    'ADULT':'2',
    'CURRENCY':'4',
    'CHILD':'0',
    'TOWNTO_ANY':'1',
    'TOWNTO':'',
    'STARS_ANY':'1',
    'STARS':'',
    'hotelsearch':'0',
    'HOTELS_ANY':'1',
    'HOTELS':'',
    'MEAL':'',
    'FREIGHT':'0',
    'FILTER':'0',
    'MOMENT_CONFIRM':'0',
    'HOTELTYPES':'',
    'PACKET':'0',
    'PRICEPAGE':1})
    g.go(url + qs)
    response = str(g.response.body)
    return response




while i == -1:
    print i
    ss = loadPage('http://online.siesta.kiev.ua/search_tour?',i)
     # str = u'Данных не найдено. Измените параметры поиска'
    # k = new_string.find(str)
    i= i + 1















