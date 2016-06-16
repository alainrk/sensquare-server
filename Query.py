import mysql.connector

'''
Query utili d'esempio:

>>> r = list(p.getAllRulesForSensor(100))
>>> a = list(map(lambda x: list(x), r))
>>> b = list(filter(lambda x: x[0]<10, a))
>>> b
[[9, 100, 'Default Audio', '32TPQ8628029570', 4, 999999999, 999999999999999999, 1800, 1465913543]]

########

select name, mgrs, timestamp, value, mgrs_filter, sensors.type as sensor_id from all_sensor_data join sensors on all_sensor_data.type = sensors.type where sensors.type=6;

'''

class Query:
    conn = None
    cursor = None

    def __init__(self):
        db, user, passw, host = tuple(map(lambda x:x.strip("\n").split(":")[1], open("auth.txt", "r").readlines()))
        self.conn = mysql.connector.connect(user=user, password=passw, database=db, host=host)

    def getAllSensors(self):
        self.cursor = self.conn.cursor()
        res = self.cursor.execute("select * from sensors")
        return self.cursor

    # Minimum granularity and time comprehensive the given coord
    def getFinestRule(self, sensor, mgrs_client):
            self.cursor = self.conn.cursor()
            res = self.cursor.execute("select * from rules")
            return self.cursor

    def getAllRules(self):
            self.cursor = self.conn.cursor()
            res = self.cursor.execute("select * from rules")
            return self.cursor

    def getAllRulesForSensor(self, sensor):
            self.cursor = self.conn.cursor()
            res = self.cursor.execute("select * from rules where type=%s", (sensor,))
            return self.cursor

    def insertInAllSensorData(self, user, sensor, latitude, longitude, mgrs, value, timest):
        try:
            self.cursor = self.conn.cursor()
            query = "INSERT INTO all_sensor_data(user, type, latitude, longitude, mgrs, value, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            res = self.cursor.execute(query, (user, sensor, latitude, longitude, mgrs, value, timest))
        except mysql.connector.Error as err:
            print("DB ERROR: {}".format(err))

    def insertInAllWifiData(self, user, ssid, latitude, longitude, mgrs, bssid, strength, timestamp):
        try:
            self.cursor = self.conn.cursor()
            query = "INSERT INTO all_wifi_data(user, ssid, latitude, longitude, mgrs, bssid, strength, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            res = self.cursor.execute(query, (user, ssid, latitude, longitude, mgrs, bssid, strength, timestamp))
        except mysql.connector.Error as err:
            print("DB ERROR: {}".format(err))

    def insertInAllTelData(self, user, latitude, longitude, mgrs, timestamp, strength, operator, tech):
        try:
            self.cursor = self.conn.cursor()
            query = "INSERT INTO all_tel_data(user, latitude, longitude, mgrs, timestamp, strength, operator, tech) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            res = self.cursor.execute(query, (user, latitude, longitude, mgrs, timestamp, strength, operator, tech))
        except mysql.connector.Error as err:
            print("DB ERROR: {}".format(err))

    def close(self):
        self.cursor.close()
        self.conn.commit()
        self.conn.close()
