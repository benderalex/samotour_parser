# -*- coding: utf-8 -*-
import os
from pyquery import PyQuery as pq
import re, itertools
import MySQLdb
from datetime import datetime

start = datetime.now()

global_path = "grab"
files = []
dataPattern = re.compile(r'(\d{1,2}).(\d{1,2}).(\d{4})')
mealPattern = re.compile(r'^(\w{1,3})')
peoplePattern = re.compile(r'^(\d{1})')
country = {'Turkey': {'joinup': '8', 'tourbox': '46', 'currency': '2'},
           'Egypt': {'joinup': '9', 'tourbox': '54', 'currency': '2'},
           'Kipr': {'joinup': '50', 'tourbox': '36', 'currency': '2'},}


db = MySQLdb.connect("localhost", "root", "alex", "tourbox_com_ua", charset='utf8')


def files_by_path(path):
    for file in os.listdir(path):
        if file.endswith(".html"):
            files.append(file)
            body = open(path+'/'+file, 'r').read().decode('cp1251')
            print file
            response = body[body.find('<table'):len(body)]
            parss(response)
    return files



def find_country(find):
    for key in country:
        if country[key]['tcc'] == find:
            return country[key]['tourbox']




def parss(page_send):
    if not page_send:
        print "clear"
    elif page_send.find('error') > 0:
        print 'system error'
    elif page_send.find('recaptcha') > 0:
        print 'capcha'
    elif len(page_send) < 10:
        print 'clear file'
    else:
        sss = pq(page_send).find('tr:gt(0)')
        for tr in sss('tr').items():
            child = clear_string(tr.attr('data-child'))
            adult = clear_string(tr.attr('data-adult'))

            data = clear_string(tr('td:eq(0)').text())

            search_result = dataPattern.search(data.encode('utf8')).groups()
            date = '-'.join(reversed(search_result))

            tur = clear_string(tr('td:eq(1)').text().encode('utf8'))
            nights = clear_string(tr.attr('data-nights'))
            hotel = clear_string(tr('td:eq(4)').text()).encode('utf8')

            # meal_from_file = clear_string(tr('td:eq(6)').text())
            # meal = mealPattern.search(meal_from_file).group().encode('utf8')

            meal = clear_string(tr('td:eq(5)').text())

            country_from_body = clear_string(tr.attr('data-state'))
            room = clear_string(tr('td:eq(6)').text()).encode('utf8')
            price = clear_string(tr('td:eq(9)').text())
            dt = clear_string(tr.attr('data-ptype'))
            insert_db(tur, nights, hotel, meal, room, adult, child, price, date, find_country(country_from_body), 3)
            # print clear_string(tur)
            # print hotel, room, child, adult, child, meal
            print hotel, dt




def find_country(find):
    for key in country:
        if country[key]['joinup'] == find:
            return country[key]['tourbox']


def insert_db(tour_name, nights, hotel, pitanie, room, adults, child, price, date, country, id):
    with db:
        cursor = db.cursor()
        sql = '''INSERT INTO tours_parser(tour, nights, hotel, meal, room, adults, child, price, departure_date, country_id, operator_id) \
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        cursor.execute(sql, (tour_name, nights, hotel, pitanie, room, adults, child, price, date, country, id))




def clear_string(str):
    data_from_file = re.sub(r'\\n\\', '', str)
    clear_data = re.sub(r'  ', '', data_from_file)
    clear_data = re.sub(r'\\', '', clear_data)
    clear_data = re.sub(r'"', '', clear_data)
    str = u'Питание по программе'
    clear_data = re.sub(str, 'PRM meal', clear_data)
    return clear_data


# files_by_path("joinup_turkey_2_0")
files_by_path("joinup_all/egypt_1_0")
files_by_path("joinup_all/egypt_2_0")
files_by_path("joinup_all/egypt_3_0")
files_by_path("joinup_all/egypt_2_1")

files_by_path("joinup_all/kipr_1_0")
files_by_path("joinup_all/kipr_2_0")
files_by_path("joinup_all/kipr_3_0")
files_by_path("joinup_all/kipr_2_1")


db.close()

end = datetime.now()

ss = end-start

print ss