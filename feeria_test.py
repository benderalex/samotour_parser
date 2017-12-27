# -*- coding: utf-8 -*-
from grab import Grab
from urllib import urlencode
from pyquery import PyQuery as pq
import urllib2
import pprint
import re, itertools
import MySQLdb

id_op = 3
country_id_opetator = 6
country_box = 85
adult_par = 3
child_par = 0
operator_url = 'http://samo.feeria.ua/search_tour?'

countries = [33]


adults = [
{'adult':1, 'child': 0},
{'adult':2, 'child': 0},
{'adult':3, 'child': 0},
{'adult':2, 'child': 1}]

db = MySQLdb.connect("localhost", "root", "alex", "tourbox_com_ua", charset='utf8')

dataPattern = re.compile(r'(\d{1,2}).(\d{1,2}).(\d{4})')
mealPattern = re.compile(r'^(\w{1,3})')
peoplePattern = re.compile(r'^(\d{1})')



def loadPage(url, adult, child, country, i):
    print 'run Grab'
    g = Grab()
    g.setup(log_dir='feeria')
    g.setup(timeout=250, connect_timeout=200)
    g.setup(proxy='220.101.93.3:3128', proxy_type='http')
    qs = urlencode({'samo_action':'PRICES',
    'TOWNFROMINC':'2',
    'STATEINC':country,
    'TOURINC':'0',
    'CHECKIN_BEG':'20160801',
    'NIGHTS_FROM':'3',
    'CHECKIN_END':'20160831',
    'NIGHTS_TILL':'14',
    'ADULT':adult,
    'CURRENCY':'1',
    'CHILD':child,
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

def parss(page_send):
    print 'run parser'

    page = page_send
    new_page = page
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

        insert_db(tur, nights, '', hotel, meal, room, adult, child, price, date, country_box, id_op)
        print tur
        # print date
        # print hotel
        # print meal
        # print room
        # print adult
        # print child
        # print price






def parametrs_generator():
    print 'run parametrs'
    new_list = []
    for country in countries:
        for peoples in adults:
           params = {'adult':peoples['adult'],'child': peoples['child'], 'country':country,}
           new_list.append(params)
    return new_list



def generator_url():
    print 'run generator url'
    parametrs_list = parametrs_generator()
    i=1
    k = -1
    str = u'Данных не найдено. Измените параметры поиска'
    ss = []
    while k == -1:
        print adult_par, child_par, country_id_opetator, i
        stran = loadPage('http://samo.feeria.ua/search_tour?', adult_par, child_par, country_id_opetator, i)
        ss.append(stran)
        new_sring = stran.decode('cp1251')
        k = new_sring.find(str)
        parss(new_sring)
        i = i + 1




generator_url()





db.close()