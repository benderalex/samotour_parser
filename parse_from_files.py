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
    elif page_send.find('recaptcha') > 0:
        print 'capcha'
    else:
        sss = pq(page_send).find('tr:gt(0)')
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

            country_from_body = clear_string(tr.attr('data-state'))
            room = clear_string(tr('td:eq(5)').text()).encode('utf8')
            price = clear_string(tr('td:eq(8)').text())

            insert_db(tur, nights, hotel, meal, room, adult, child, price, date, find_country(country_from_body), 2)
            print tur, hotel, meal


def find_country(find):
    for key in country:
        if country[key]['tcc'] == find:
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


files_by_path("tcc_dominicana_1_0")
files_by_path("tcc_dominicana_2_0")
files_by_path("tcc_dominicana_3_0")
files_by_path("tcc_dominicana_2_1")


files_by_path("tcc_tayland_1_0")
files_by_path("tcc_tayland_2_0")
files_by_path("tcc_tayland_3_0")
files_by_path("tcc_tayland_2_1")

files_by_path("tcc_vietnam_1_0")
files_by_path("tcc_vietnam_2_0")
files_by_path("tcc_vietnam_3_0")
files_by_path("tcc_vietnam_2_1")



db.close()

end = datetime.now()

ss = end-start

print ss