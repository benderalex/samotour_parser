from selenium import webdriver
from selenium.webdriver.common.proxy import *

myProxy = "168.1.47.248:8080"

driver = webdriver.Firefox()
driver.get('http://online.joinup.ua/search_tour?PRICEPAGE=264&PACKET=0&CURRENCY=2&STARS_ANY=0&CHECKIN_BEG=20160802&TOWNTO=&TOURINC=0&TOWNFROMINC=18&FREIGHT=0&MEAL=&ADULT=2&samo_action=PRICES&TOWNTO_ANY=1&MOMENT_CONFIRM=0&hotelsearch=0&NIGHTS_TILL=7&STARS=2%2C3%2C4&HOTELS=&FILTER=1&HOTELTYPES=&CHECKIN_END=20160831&STATEINC=8&CHILD=0&HOTELS_ANY=1&PROGRAMINC=0&NIGHTS_FROM=7')
elem = driver.find_element_by_xpath("//*")
source_code = elem.get_attribute("outerHTML")
f = open('selenium/html_source_code', 'w')
f.write(source_code.encode('utf-8'))
f.close()


