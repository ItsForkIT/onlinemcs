# District Calculator

f = open('district.txt','r')
print 'Enter the Latitude:'
lati = float(raw_input())
print 'Enter the Longitude:'
longi = float(raw_input())
x = f.readline()
y = x.split(',')
olat = y[2][2:-3]
olong = y[3][2:-3]
minLat = 100
minLong = 100
i = 0 
while i<942:
	x = f.readline()
	y = x.split(',')
	olat = y[2][2:-3]
	olong = y[3][2:-3]

	if((abs(lati - float(olat)) < minLat) and (abs(longi - float(olong)) < minLong)):
		#print 'True:' + str(abs(lati-float(olat))) + '<' + str(minLat)
		#print 'Lat: '+ str(minLat) + 'Long:'+ str(minLong) + 'City:' + city
		minLat = abs(lati - float(olat))
		minLong = abs(longi - float(olong))
		city = y[1]
	i = i + 1

print 'Final Result:'
print 'Min Lat Diff: '+ str(minLat) + 'Min Long Diff:'+ str(minLong) + 'City:' + city