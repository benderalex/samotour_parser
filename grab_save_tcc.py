# -*- coding: utf-8 -*-
from grab import Grab
from urllib import urlencode
from pyquery import PyQuery as pq
import urllib2
import pprint
import re, itertools
import MySQLdb
from datetime import datetime

start = datetime.now()


country = {'Barbados': {'tcc': '42', 'tourbox': '5', 'currency':'2'},
'Brasil': {'tcc': '35', 'tourbox': '7', 'currency':'2'},
'Vietnam': {'tcc': '26', 'tourbox': '18', 'currency':'2'},
'Dominicana': {'tcc': '14', 'tourbox': '1', 'currency':'2'},
'Indonesy': {'tcc': '8', 'tourbox': '17', 'currency':'2'},
'Kenya': {'tcc': '21', 'tourbox': '23', 'currency':'2'},
'Cuba': {'tcc': '15', 'tourbox': '2', 'currency':'2'},
'Mavrikiy': {'tcc': '6', 'tourbox': '13', 'currency':'3'},
'Maldives': {'tcc': '13', 'tourbox': '26', 'currency':'2'},
'Mexico': {'tcc': '16', 'tourbox': '3', 'currency':'2'},
'Seyshel': {'tcc': '11', 'tourbox': '12', 'currency':'3'},
'Tayland': {'tcc': '12', 'tourbox': '22', 'currency':'2'},
'Filiphines': {'tcc': '49', 'tourbox': '0', 'currency':'2'},
'Polineziya': {'tcc': '91', 'tourbox': '26', 'currency':'3'},
'Shri-Lank': {'tcc': '17', 'tourbox': '15', 'currency':'2'},
'Yamayka': {'tcc': '58', 'tourbox': '4', 'currency':'2'}}

adult = 2
child = 0
country_op = country['Tayland']['tcc']






def loadPage(url, adult, child, country, i):
    print 'run Grab'
    g = Grab()
    g.setup(log_dir='grab')
    g.setup(timeout=250, connect_timeout=200)
    g.setup(proxy='54.183.238.208:8083', proxy_type='http')
    qs = urlencode({'samo_action':'PRICES',
                    'TOWNFROMINC':'101',
                    'STATEINC':country_op,
                    'TOURTYPE':'0',
                    'TOURINC':'0',
                    'CHECKIN_BEG':'20160806',
                    'NIGHTS_FROM':'2',
                    'CHECKIN_END':'20160810',
                    'NIGHTS_TILL':'10',
                    'ADULT':'2',
                    'CURRENCY':'2',
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
    captcha = ''
    ss = []
    while k==-1:
        print adult, child, country_op, i
        stran = loadPage('http://tcc.com.ua/online/search_tour?', adult, child, country_op, i)
        ss.append(stran)
        new_sring = stran.decode('cp1251')
        k = new_sring.find(str)
        i = i + 1



generator_url()


end = datetime.now()

ss = end-start

print ss