import csv
import sys
import json
from firebase import firebase
import datetime
#mi objeto de firebase
firebase = firebase.FirebaseApplication('https://haha-4cf04.firebaseio.com', None)
     
data = []

#LEYENDO INFO DEL CSV 
with open('/mnt/d/offlinemcs/yourBigFile3.csv')as csvfile:
	read = csv.reader(csvfile)
	i=0
	for row in read:
		size =int(row[0])
		type = (row[1]).replace(" ","")
		tlt = int(row[2])	
		category =(row[3]).replace(" ","")
		sender = int(row[4])
		reciver = str(row[5]).replace(" ","")
		lat = float(row[6])
		long1 = float(row[7])
		datetime = int(row[8])
		group =int(row[9])
		name =str(str(type)+'_'+str(tlt)+'_'+str(category)+'_'+str(sender)+'_'+str(reciver)+'_'+str(lat)+'_'+str(long1)+'_'+str(datetime)+'_'+str(group))
		text="NULL"
		#dateTime = datetime.datetime.strptime(dateTime, "%Y/%m/%d %H:%M:%S")
		#print str(dateTime1) + '->' + str(dateTime)
		i=i+1
		
		firebase.put('/onlineMCS',i,{"name": name,"type": type,"tlt": tlt,"category": category,"sender": sender,"reciver": reciver,"lat": lat,"long": long1,"datetime": datetime, "group": group,"size":size})
