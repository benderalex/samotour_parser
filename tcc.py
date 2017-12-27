# -*- coding: utf-8 -*-
from grab import Grab
from urllib import urlencode
from pyquery import PyQuery as pq
import urllib2
import pprint
import re, itertools
import MySQLdb

countries = [20,30,40]
adults = [
{'adult':1, 'child': 0},
{'adult':2, 'child': 0},
{'adult':3, 'child': 0},
{'adult':2, 'child': 1}]

db = MySQLdb.connect("localhost", "root", "alex", "tourbox_com_ua", charset='utf8')

dataPattern = re.compile(r'(\d{1,2}).(\d{1,2}).(\d{4})')
mealPattern = re.compile(r'^(\w{1,3})')
peoplePattern = re.compile(r'^(\d{1})')



def loadPage(url, i):
    g = Grab()
    g.setup(log_dir='grab')
    g.setup(timeout=150, connect_timeout=100)
    # g.setup(proxy='186.170.31.134:8080', proxy_type='http')
    # qs = urlencode({'samo_action':'PRICES',
    # 'TOWNFROMINC':'101',
    # 'STATEINC':'33',
    # 'TOURTYPE':'0',
    # 'TOURINC':'963',
    # 'CHECKIN_BEG':'20160721',
    # 'NIGHTS_FROM':'2',
    # 'CHECKIN_END':'20160722',
    # 'NIGHTS_TILL':'10',
    # 'ADULT':'2',
    # 'CURRENCY':'1',
    # 'CHILD':'0',
    # 'TOWNTO_ANY':'1',
    # 'TOWNTO':'',
    # 'STARS_ANY':'1',
    # 'STARS':'',
    # 'hotelsearch':'0',
    # 'HOTELS_ANY':'1',
    # 'HOTELS':'',
    # 'MEAL':'',
    # 'FREIGHT':'0',
    # 'FILTER':'0',
    # 'HOTELTYPES':'',
    # 'PACKET':'1',
    # 'PRICEPAGE':i})
    # g.go(url + qs)
    g.go(url)
    body = g.response.body
    response = body[body.find('<table'):len(body)]
    return response

def clear_string(str):
    data_from_file = re.sub(r'\\n\\', '', str)
    clear_data = re.sub(r'  ', '', data_from_file)
    clear_data = re.sub(r'\\', '', clear_data)
    clear_data = re.sub(r'"', '', clear_data)
    clear_data = re.sub(r' UAH', '', clear_data)
    return clear_data


def insert_db(tour_name, nights, city, hotel, pitanie, room, adults, child, price, date, country, id):
    with db:
        cursor = db.cursor()
        sql = '''INSERT INTO tours_parse(tur, nights, city, hotel, pitanie, room, adults, children, price, departure_date, country, tourop_id) \
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        cursor.execute(sql, (tour_name, nights, city, hotel, pitanie, room, adults, child, price, date, country, id))



def parsing():
    page = loadPage(
        'online.siesta.kiev.ua/search_tour?samo_action=PRICES&TOWNFROMINC=5&STATEINC=26&TOURINC=0&PROGRAMGROUPINC=0&PROGRAMINC=0&CHECKIN_BEG=20160728&NIGHTS_FROM=10&CHECKIN_END=20160808&NIGHTS_TILL=10&ADULT=3&CURRENCY=4&CHILD=0&TOWNTO_ANY=1&TOWNTO=&STARS_ANY=1&STARS=&hotelsearch=0&HOTELS_ANY=1&HOTELS=&MEAL=&FREIGHT=0&FILTER=0&MOMENT_CONFIRM=0&HOTELTYPES=&PACKET=0&PRICEPAGE=2&rev=3652072884&_=1469271694994',
        1)
    new_page = page.decode('cp1251')
    sss = pq(new_page).find('tr:gt(0)')

    for tr in sss('tr').items():
        child = clear_string(tr.attr('data-child'))
        adult = clear_string(tr.attr('data-adult'))

        data = clear_string(tr('td:eq(0)').text())

        search_result = dataPattern.search(data.encode('utf8')).groups()
        date = '-'.join(reversed(search_result))

        tur = tr('td:eq(1)').text().encode('utf8')
        nights = tr('td:eq(2)').text()
        hotel = clear_string(tr('td:eq(3)').text()).encode('utf8')

        meal_from_file = clear_string(tr('td:eq(4)').text())
        meal = mealPattern.search(meal_from_file).group().encode('utf8')

        room = clear_string(tr('td:eq(5)').text()).encode('utf8')
        price = clear_string(tr('td:eq(9)').text())

        insert_db(tur, nights, '', hotel, meal, room, adult, child, price, date, 46, 2)
        print (tur)




def parametrs_generator():
    new_list = []
    for country in countries:
        for peoples in adults:
           params = {'adult':peoples['adult'],'child': peoples['child'], 'country':country,}
           new_list.append(params)
    return new_list







k = -1
i = 1
str = u'Данных не найдено. Измените параметры поиска'

# while k == -1:
    # ss = loadPage('http://tcc.com.ua/online/search_tour?',i)
    # new_sring = ss.decode('cp1251')
    # k = new_sring.find(str)
    # print i
    # print k
    # i+=1
    #






db.close()
