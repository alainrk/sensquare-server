import mysql.connector

'''
Usage

>>> from querytest import *
>>> query = Query()
>>> datas = query.getAllSensors()

>>> for i in datas:
...    print (i)
...
(5, 'Light', 12)
(6, 'Pressure', 8)
(12, 'Humidity', 11)
(13, 'Temperature', 10)
(100, 'Audio Amplitude', 12)
(101, 'WiFi', 13)
(102, 'Tel', 13)
(989, 'Pippo', 12)
(999, 'Puppo', 12)

>>> query.close()


'''

# cnx = mysql.connector.connect(user='pydroid', password='pydroid', database='crowdroid')
# cursor = cnx.cursor()

######################################################

# cursor.execute("insert into sensors (type, name, mgrs_filter) values (%s, %s, %s)", (12, "Humidity", 11))
# cursor.execute("insert into sensors (type, name, mgrs_filter) values (%s, %s, %s)", (13, "Temperature", 10))
# cursor.execute("insert into sensors (type, name, mgrs_filter) values (%s, %s, %s)", (100, "Audio Amplitude", 12))
# cursor.execute("insert into sensors (type, name, mgrs_filter) values (%s, %s, %s)", (101, "WiFi", 13))
# cursor.execute("insert into sensors (type, name, mgrs_filter) values (%s, %s, %s)", (102, "Tel", 13))
#
#
# cnx.commit()
# cursor.close()
# cnx.close()

######################################################

# par = "e"
# cursor.execute("select * from sensors where name like (%s)", ("%" + par + "%",))
#
# for c in cursor:
#     print(c)
#
# cnx.commit()
# cursor.close()
# cnx.close()

######################################################

# cursor.execute("UPDATE sensors SET name='Puppo' WHERE name=%s AND type=%s", ("Pippo",999))
#
# cnx.commit()
# cursor.close()
# cnx.close()

######################################################

class Query:
    conn = None
    cursor = None

    def __init__(self):
        self.conn = mysql.connector.connect(user='pydroid', password='pydroid', database='crowdroid')

    def getAllSensors(self):
        self.cursor = self.conn.cursor()
        res = self.cursor.execute("select * from sensors")
        return self.cursor

    def close(self):
        self.cursor.close()
        self.conn.commit()
        self.conn.close()
