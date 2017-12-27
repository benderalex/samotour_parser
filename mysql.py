import MySQLdb
import time

today = time.strftime("%Y-%m-%d")

db = MySQLdb.connect("localhost", "root", "alex", "tourbox_com_ua")


def insert_db(tour_name, nights, city, hotel, pitanie, room, adults, child, price, date, country, id):
    with db:
        cursor = db.cursor()
        sql = '''INSERT INTO tours_parse(tur, nights, city, hotel, pitanie, room, adults, children, price, departure_date, country, tourop_id) \
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        cursor.execute(sql, (tour_name, nights, city, hotel, pitanie, room, adults, child, price, date, country, id))



insert_db('dasasd',7,'city','hotel', 'pitanie', 'room', 2, 0, '1800', '2015-06-06', 46, 2)