# -*- coding: utf-8 -*-
from grab import Grab
from urllib import urlencode
from pyquery import PyQuery as pq
import urllib2
import pprint
import re, itertools
import MySQLdb
from random import randint
from datetime import datetime

start = datetime.now()


country = {'Turkey': {'joinup': '8', 'tourbox': '46', 'currency':'2'},
           'Egypt': {'joinup': '9', 'tourbox': '54', 'currency': '2'},
           'Kipr': {'joinup': '50', 'tourbox': '36', 'currency': '2'},}

adult = 2
child = 1
country_name = 'Kipr'
country_op = country[country_name]['joinup']
operator_url = 'http://online.joinup.ua/search_tour?'





def loadPage(url, adult, child, country, i):
    print 'run Grab'
    con = randint(201, 387)
    con2 = randint(358, 482)
    g = Grab()
    g.setup(log_dir='joinup_all/kipr_2_1')
    g.setup(timeout=con, connect_timeout=con2)
    g.setup(proxy='220.101.93.3:3128', proxy_type='http')
    qs = urlencode({'samo_action':'PRICES',
                    'TOWNFROMINC':'18',
                    'STATEINC':country_op,
                    'TOURINC':'0',
                    'PROGRAMINC':'0',
                    'CHECKIN_BEG':'20160805',
                    'NIGHTS_FROM':'7',
                    'CHECKIN_END':'20160831',
                    'NIGHTS_TILL':'14',
                    'ADULT':adult,
                    'CURRENCY':'2',
                    'CHILD':child,
                    'TOWNTO_ANY':'1',
                    'TOWNTO':'',
                    'STARS_ANY':'0',
                    'STARS':'2,3,4',
                    'hotelsearch':'0',
                    'HOTELS_ANY':'1',
                    'HOTELS':'',
                    'MEAL':'',
                    'FREIGHT':'0',
                    'FILTER':'1',
                    'MOMENT_CONFIRM':'0',
                    'HOTELTYPES':'',
                    'PACKET':'0',
                    'PRICEPAGE':i})
    print (url + qs)
    g.go(url + qs)
    body = g.response.body
    return body



def generator_url():
    print 'run generator url'
    i=1
    k = -1
    str = u'Данных не найдено'
    ss = []
    while k==-1:
        print adult, child, country_name, i
        stran = loadPage(operator_url, adult, child, country_op, i)
        ss.append(stran)
        new_sring = stran.decode('cp1251')
        k = new_sring.find(str)
        i = i + 1



generator_url()


end = datetime.now()

ss = end-start

print ss