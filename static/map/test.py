# District Calculator

f = open('district1.txt','r')
lati = 23.54
longi = 87.29
x = f.readline()
y = x.split(',')
olat = y[2][2:-3]
olong = y[3][2:-3]
minLat = 100
minLong = 100
city = 'Durgapur'
print 'Lat: '+ str(olat) + 'Long:'+ str(olong) + 'City:' + city
i = 0 
while i<88:
	x = f.readline()
	y = x.split(',')
	olat = y[2][2:-3]
	olong = y[3][2:-3]

	if((abs(lati - float(olat)) < minLat) and (abs(longi - float(olong)) < minLong)):
		print 'Lat: '+ str(minLat) + 'Long:'+ str(minLong) + 'City:' + city
		minLat = olat
		minLong = olong
		city = y[1]
	i = i + 1

print 'Final Result:'
print 'Lat: '+ str(minLat) + 'Long:'+ str(minLong) + 'City:' + city