# -*- coding: iso-8859-15 -*-
import sqlite3

'''
USAGE Examples

queryObj = Query()
queryObj.updateFoo(par1, par2)
queryObj.close()

queryObj = Query()
req = queryObj.getStuff()
for row in req:
	doStuff(row[0], par, par2)
queryObj.close()

'''

class Query:

	conn = None

	def __init__(self):
		self.conn = sqlite3.connect("db.sqlite")

	def insertInAllSensorData(self, user, type_id, latitude, longitude, mgrs, value, timest):
		cur = self.conn.cursor()
		query = "INSERT INTO all_sensor_data(user, type, lat, long, mgrs, value, timest) VALUES (?, ?, ?, ?, ?, ?, ?)"
		#print(query)
		print ("Query users: ", cur.execute(query, (user, type_id, latitude, longitude, mgrs, value, timest)))
		self.conn.commit()

	def insertInAllWifiData(self, user, ssid, latitude, longitude, mgrs, bssid, rssi, timest):
		cur = self.conn.cursor()
		query = "INSERT INTO all_wifi_data(user, ssid, lat, long, mgrs, bssid, rssi, timest) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
		#print(query)
		print ("Query users: ", cur.execute(query, (user, ssid, latitude, longitude, mgrs, bssid, rssi, timest)))
		self.conn.commit()

	def insertInAllTelData(self, user, latitude, longitude, mgrs, time, sinr, operator, tech):
		cur = self.conn.cursor()
		query = "INSERT INTO all_tel_data(user, lat, long, mgrs, timest, sinr, operator, tech) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
		#print(query)
		print ("Query users: ", cur.execute(query, (user, latitude, longitude, mgrs, time, sinr, operator, tech)))
		self.conn.commit()

	# def insertNewUser(self, chatId, isGroup, titleOrUsername, date_start):
	# 	cur = self.conn.cursor()
	# 	print "Query users: ", cur.execute("INSERT INTO users(chatId, isGroup, titleOrUsername, date_start) \
	# 		SELECT "+str(chatId)+", "+str(isGroup)+", '"+titleOrUsername+"', "+str(date_start)+" \
	# 		WHERE not exists(SELECT 1 FROM users WHERE chatId = "+str(chatId)+")")
    #
	# 	print "Query subscribes: ", cur.execute("INSERT INTO subscribes(chatId, scioperiFeed) \
	# 		SELECT "+str(chatId)+", 1 \
	# 		WHERE not exists(SELECT 1 FROM subscribes WHERE chatId = "+str(chatId)+")")
    #
	# 	self.conn.commit()
    #
	# def updateScioperiFeedForUser(self, onOff, chatId):
	# 	cur = self.conn.cursor()
	# 	print "Query update Subscription: ", cur.execute("UPDATE subscribes SET scioperiFeed = ? WHERE chatId = ?", (onOff, chatId))
	# 	self.conn.commit()
    #
	# def getScioperiSubcribers(self):
	# 	cur = self.conn.cursor()
	# 	req = cur.execute("SELECT users.chatId from users,subscribes WHERE scioperiFeed = 1 AND users.chatId = subscribes.chatId")
	# 	print "Get Scioperi Subscribers: ", req
	# 	self.conn.commit()
	# 	return req
    #
	# def getUsers(self):
	# 	cur = self.conn.cursor()
	# 	req = cur.execute("SELECT users.chatId from users")
	# 	print "Get Scioperi Subscribers: ", req
	# 	self.conn.commit()
	# 	return req
    #
	# def getFermateByLineaDenomUbicOLD(self, linea, matchString, verso):
	# 	cur = self.conn.cursor()
	# 	#req = cur.execute("SELECT codice_fermata, codice_linea, denominazione, ubicazione FROM lineefermate WHERE codice_linea = "+str(linea)+" AND (denominazione like '%"+matchString+"%' OR ubicazione like '%"+matchString+"%')")
	# 	req = cur.execute("SELECT codice_fermata, codice_linea, denominazione, ubicazione FROM lineefermate \
	# 		WHERE codice_linea = ? AND (denominazione like ? OR ubicazione like ?)", (linea, '%'+matchString+'%', '%'+matchString+'%'))
	# 	print "Get FermateByLineaDenomUbic: ", req
	# 	self.conn.commit()
	# 	return req
    #
	# def getCapolineaByLinea(self, linea):
	# 	cur = self.conn.cursor()
	# 	req = cur.execute("SELECT DISTINCT denominazione_capolinea FROM Fermate_Linee_Capolinea WHERE codice_linea = ? GROUP BY denominazione_capolinea", (linea,))
	# 	print "Get getCapolineaByLinea: ", req
	# 	self.conn.commit()
	# 	return req
    #
	# def getNomeLinea(self, linea):
	# 	cur = self.conn.cursor()
	# 	req = cur.execute("SELECT route_long_name FROM routes WHERE route_id = ?", (linea,))
	# 	print "Get getNomeLinea: ", req
	# 	self.conn.commit()
	# 	return req
    #
	# def getVersoByCapolineaAndLinea(self, capolinea, linea):
	# 	cur = self.conn.cursor()
	# 	req = cur.execute("SELECT DISTINCT verso FROM Fermate_Linee_Capolinea WHERE denominazione_capolinea LIKE ? and codice_linea = ?", (capolinea,linea))
	# 	print "Get getVersoByCapolineaAndLinea: ", req
	# 	self.conn.commit()
	# 	return req
    #
	# def getFermateByLineaDenomUbic(self, linea, matchString, verso):
	# 	cur = self.conn.cursor()
	# 	matchString = matchString.encode('utf-8')
	# 	matchString = matchString.replace('\'','`').replace('à','').replace('è','').replace('é','').replace('ì','').replace('ò','').replace('ù','')
	# 	print "------------ "+matchString+" -------------------"
	# 	req = cur.execute("SELECT DISTINCT codice_fermata, codice_linea, denominazione, ubicazione FROM Fermate_Linee_Capolinea \
	# 		WHERE codice_linea = ? AND verso = ? AND (denominazione like ? OR ubicazione like ?)", (linea, verso, '%'+matchString+'%', '%'+matchString+'%'))
	# 	print "Get FermateByLineaDenomUbic: ", req
	# 	self.conn.commit()
	# 	return req
    #
	# def getLocationFermata(self, fermata):
	# 	cur = self.conn.cursor()
	# 	req = cur.execute("SELECT latitudine, longitudine FROM fermate WHERE codice = ?", (fermata,))
	# 	print "getLocationFermata: ", req
	# 	self.conn.commit()
	# 	return req

	def close(self):
		self.conn.close()
