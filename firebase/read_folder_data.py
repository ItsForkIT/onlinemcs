import os
p = open("path.txt","r")
path = p.read()
f1 = open("d1.txt","w") #read the folder info and store the name
x = os.listdir(path)
for files in x:
	z= str(os.path.getsize(path + files))
	if files.startswith('Map'):
		print "NULL";
	elif files.startswith('NULL'):
		print "NULL"
	else:
		f1.write(z +', ')  #size of the file 
		f1.write(files)
		f1.write('\n')
f1.close()
f1 = open('d1.txt', 'r')
f2 = open('yourBigFile.txt', 'w')
for line in f1:
    f2.write(line.replace('_', ', ').replace('.jpg', ' ').replace('.txt', ' ').replace('.3gp', ' ')) # divide the name field into there orignal field
f1.close()
f2.close()

#convert txt file to csv
import csv
with open('yourBigFile.txt', 'r') as in_file:
    stripped = (line.strip() for line in in_file)
    lines = (line.split(",") for line in stripped if line)
    with open('mydata1.csv', 'w') as out_file:
        writer = csv.writer(out_file)
        writer.writerows(lines)

# Create a difference file  

import csv
f1 = open ("mydata1.csv")
oldFile1 = csv.reader(f1)
oldList1 = []
for row in oldFile1:
    oldList1.append(row)

f2 = open ("mydata.csv")
oldFile2 = csv.reader(f2)
oldList2 = []
for row in oldFile2:
    oldList2.append(row)

f1.close()
f2.close()

f1 = open("def.csv","w")
f1.write(str([row for row in oldList1 if row not in oldList2]))
f1.close()

f1 = open('def.csv', 'r')
f2 = open('def1.csv', 'w')
for line in f1:
    f2.write(line.replace(' [', '\n').replace('],', '').replace("'", " ").replace(',   ', ', ').replace(' ,', ',').replace(']]', '').replace('[[ ', '')) # divide the name field into there orignal field
f1.close()
f2.close()


#insert data into the firebase database
import csv
import sys
import json
from firebase import firebase
import datetime
firebase = firebase.FirebaseApplication('https://haha-4cf04.firebaseio.com', None) # firebase link
data = []
f1 = open("lastvalue.txt","r")
i=int(f1.read())
f1.close()
print i
if os.path.getsize("def1.csv") > 2:
	with open('def1.csv')as csvfile: 
		read = csv.reader(csvfile)
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
				f1=open(path +str(name))
				content=f1.read()
				f1.close()
			print name
			firebase.put('/onlineMCS',i,{"name": name,"type": type,"tlt": tlt,"category": category,"sender": sender,"reciver": reciver,"lat": lat,"long": long1,"datetime": datetime, "group": group,"size":size,"content":content})

			f1 = open("lastvalue.txt","w")
			f1.write(str(i))
			f1.close()
#delete extra files
os.rename("mydata1.csv","mydata.csv")
os.remove("d1.txt")
os.remove("yourBigFile.txt")
os.remove("def.csv")
os.remove("def1.csv")
