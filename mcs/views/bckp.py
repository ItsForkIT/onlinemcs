
def findSimilarFiles():
	# Range query to retrieve files between dates
	minFileDateTime = Files.objects.all().aggregate(Min('DateTime')).itervalues().next()
	maxFileDateTime = Files.objects.all().aggregate(Max('DateTime')).itervalues().next()
	minFileDateTimeParsed = minFileDateTime.strftime('%Y%m%d%H%M%S')
	maxFileDateTimeParsed = maxFileDateTime.strftime('%Y%m%d%H%M%S')
#	print minFileDateTime 
#	print maxFileDateTime

	# Time Slice to divide the time
	timeSlice = 15
	noOfClusters = 0
	minDist = 100
	minmaxFileDateTime = minFileDateTime

	# Increment Counter in timeSlice
	delta = datetime.timedelta(minutes=timeSlice)
	while minFileDateTime <= maxFileDateTime:
		minmaxFileDateTime += delta
		allFilesRange = Files.objects.filter(DateTime__range=(minFileDateTime,minmaxFileDateTime))
		findSimilarPatterns(allFilesRange, minDist)
		noOfClusters += 1
		minFileDateTime = minmaxFileDateTime
		
	# Number of Clusters

def findSimilarPatterns(allFilesRange, minDist):
	
	# Compare all the elements with one another in list
	for file1,file2 in itertools.combinations(allFilesRange,2):
		splitFile1 = str(file1).split('_')
		splitFile2 = str(file2).split('_')

		if splitFile1[0] == splitFile2[0] == 'TXT':
			distance = calculateHaversineFormula(float(splitFile1[5]), float(splitFile1[6]), float(splitFile2[5]), float(splitFile2[6]))
		
			if distance < minDist:
				findContentSimilar(file1,file2,distance)
				
#	print '*************************************'

def findContentSimilar(file1, file2,distance):
	with open(os.path.join(SYNC_FOLDER,str(file1))) as f1, open(os.path.join(SYNC_FOLDER,str(file2))) as f2:
		# Read the line from similar files
		f1_line = f1.readline()
		f2_line = f2.readline()

		# Split the content of file 
		split_f1_line = f1_line.split(':')
		split_f2_line = f2_line.split(':')

		# Check whether the type of content matches
#		if split_f1_line[0] == split_f2_line[0] and split_f1_line[1] == split_f2_line[1]:
#			print str(f1_line) + ' <-----> ' + str(f2_line) +  ' <-----> ' +'Dist: ' + str(distance) + 'm'

		f1.close()
		f2.close()

def doSummarize(all_list):
	print all_list

def calculateHaversineFormula(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    distancem = 6367000 * c
    return distancem
