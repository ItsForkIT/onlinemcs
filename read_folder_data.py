import os
f1=open("d1.txt","w")
x = os.listdir('/mnt/d/DMS/sync')
for files in x:
	z= str(os.path.getsize('/mnt/d/DMS/sync/' + files))
	if files.startswith('Map'):
		print "NULL";
	elif files.startswith('NULL'):
		print "NULL"
	else:
		f1.write(z +', ')
		f1.write(files)
		f1.write('\n')
f1.close()
f1 = open('d1.txt', 'r')
f2 = open('yourBigFile.txt', 'w')
for line in f1:
    f2.write(line.replace('_', ', '))
f1.close()
f2.close()
f1 = open('yourBigFile.txt', 'r')
f2 = open('yourBigFile1.txt', 'w')
for line in f1:
    f2.write(line.replace('.jpg', ' '))
f1.close()
f2.close()
f1 = open('yourBigFile1.txt', 'r')
f2 = open('yourBigFile2.txt', 'w')
for line in f1:
    f2.write(line.replace('.txt', ' '))
f1.close()
f2.close()
f1 = open('yourBigFile2.txt', 'r')
f2 = open('yourBigFile3.txt', 'w')
for line in f1:
    f2.write(line.replace('.3gp', ' '))
f1.close()
f2.close()
import csv

with open('yourBigFile3.txt', 'r') as in_file:
    stripped = (line.strip() for line in in_file)
    lines = (line.split(",") for line in stripped if line)
    with open('mydata.csv', 'w') as out_file:
        writer = csv.writer(out_file)
        writer.writerows(lines)

import csv
import sys
import json
from firebase import firebase
import datetime
#mi objeto de firebase
firebase = firebase.FirebaseApplication('https://haha-4cf04.firebaseio.com', None)
     
data = []

#LEYENDO INFO DEL CSV 
with open('/mnt/d/onlinemcs-master/mydata.csv')as csvfile:
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
		i=i+1
		if type=='IMG':
			exp='.jpg'
		elif type=='SMS':
			exp='.txt'
		elif type=='TXT':
			exp='.txt'
		elif type=='VID':
			exp='.3gp'
		elif type=='SVS':
			exp='.3gp'
		name =str(str(type)+'_'+str(tlt)+'_'+str(category)+'_'+str(sender)+'_'+str(reciver)+'_'+str(lat)+'_'+str(long1)+'_'+str(datetime)+'_'+str(group)+str(exp))
		if name.startswith('IMG'):
			content='NULL'
		elif name.startswith('VID'):
			content='NULL'
		elif name.startswith('SVS'):
			content='NULL'
		else:
			f1=open('/mnt/d/DMS/sync/'+str(name))
			content=f1.read()
		print name
		firebase.put('/onlineMCS',i,{"name": name,"type": type,"tlt": tlt,"category": category,"sender": sender,"reciver": reciver,"lat": lat,"long": long1,"datetime": datetime, "group": group,"size":size,"content":content})
