from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, landscape, portrait
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from  reportlab.lib.styles import ParagraphStyle as PS
from  reportlab.platypus import PageBreak
from  reportlab.platypus.paragraph import Paragraph
from  reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from  reportlab.platypus.tableofcontents import TableOfContents
from  reportlab.platypus.frames import Frame
from  reportlab.lib.units import cm
from django.template import RequestContext
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from django.http import HttpResponse	
from mcs.models import *
from reportlab.lib.units import inch
from django.db.models import Max,Min
import datetime
import itertools
from math import radians, cos, sin, asin, sqrt
import os

# Show * (Subject to Moderation) if value more than threshold
subjectToModerationMin = 200
SYNC_FOLDER = "../dms/sync/"

def findSimilarFiles():
	# Range query to retrieve files between dates
	minFileDateTime = Files.objects.all().aggregate(Min('DateTime')).itervalues().next()
	maxFileDateTime = Files.objects.all().aggregate(Max('DateTime')).itervalues().next()
	minFileDateTimeParsed = minFileDateTime.strftime('%Y%m%d%H%M%S')
	maxFileDateTimeParsed = maxFileDateTime.strftime('%Y%m%d%H%M%S')
	print minFileDateTime 
	print maxFileDateTime

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
	print 'No. of Clusters : ' + str(noOfClusters)

def findSimilarPatterns(allFilesRange, minDist):
	
	# Compare all the elements with one another in list
	for file1,file2 in itertools.combinations(allFilesRange,2):
		splitFile1 = str(file1).split('_')
		splitFile2 = str(file2).split('_')

		if splitFile1[0] == splitFile2[0] == 'TXT':
			distance = calculateHaversineFormula(float(splitFile1[5]), float(splitFile1[6]), float(splitFile2[5]), float(splitFile2[6]))
		
			if distance < minDist:
				findContentSimilar(file1,file2,distance)
				
	print '*************************************'

def findContentSimilar(file1, file2,distance):
	with open(os.path.join(SYNC_FOLDER,str(file1))) as f1, open(os.path.join(SYNC_FOLDER,str(file2))) as f2:
		# Read the line from similar files
		f1_line = f1.readline()
		f2_line = f2.readline()

		# Split the content of file 
		split_f1_line = f1_line.split(':')
		split_f2_line = f2_line.split(':')

		# Check whether the type of content matches
		if split_f1_line[0] == split_f2_line[0] and split_f1_line[1] == split_f2_line[1]:
			print str(f1_line) + ' <-----> ' + str(f2_line) +  ' <-----> ' +'Dist: ' + str(distance) + 'm'

		f1.close()
		f2.close()

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

def reportGen(request):
	response = HttpResponse(content_type='application/pdf')
	doc = SimpleDocTemplate(response, pagesize=A4, rightMargin=30,leftMargin=30, topMargin=30,bottomMargin=18)
	doc.pagesize = portrait(A4)

	# Find similar files from DB
	findSimilarFiles()	

	h1 = PS(
			name = 'Heading1',
			fontSize = 14,
			leading = 30,
			leftIndent = 170)
	
	h2 = PS(
			name = 'Heading1',
			fontSize = 12,
			leading = 20,
			leftIndent = 30,
			spaceAfter = 20)

	# Table Headers
	elements = []
	elements.append(Paragraph('<b>Damage Assessment Format</b>', h1))
	elements.append(Paragraph('<i>[In-depth sectoral Assessment to have medium and long-term relief, rehabilitation and reconstruction assistance for critical sectors, assessment to be carried out by specialist]</i>',h2))


	
	context = {}
	context['Food'] =  Food.objects.values_list()
	context['FoodData'] = {}

	for listItems in context['Food']:
		if listItems[1] in context['FoodData']:
			context['FoodData'][listItems[1]] = context['FoodData'][listItems[1]] + int(listItems[2])
		else:	
			context['FoodData'][listItems[1]] = listItems[2]



	Data = [
		["<b>Food Type Requirement</b>", "<b>Information</b>", ],
	]
	
	for key, values in context['FoodData'].iteritems():
		# Subject to moderation
		if values > subjectToModerationMin:
			values = str(values) + '*'
		
		Data.append([key  , str(values)])

	Data.append(["",""])
	Data.append(["<b>Victim Affected</b>", "<b>Information</b>"])
	
	context = {}
	context['Victim'] =  Victims.objects.values_list()
	context['VictimData'] = {}

	for listItems in context['Victim']:
		if listItems[1] in context['VictimData']:
			context['VictimData'][listItems[1]] = context['VictimData'][listItems[1]] + int(listItems[2])
		else:	
			context['VictimData'][listItems[1]] = listItems[2]
		

	for key, values in context['VictimData'].iteritems():
		# Subject to moderation
		if values > subjectToModerationMin:
			values = str(values) + '*'
		Data.append([key  , str(values)])

	Data.append(["",""])
	Data.append(["<b> Health Situation</b>", "<b>Information</b>"])
	
	context = {}
	context['Health'] =  Health.objects.values_list()
	context['HealthData'] = {}

	for listItems in context['Health']:
		if listItems[1] in context['HealthData']:
			context['HealthData'][listItems[1]] = context['HealthData'][listItems[1]] + int(listItems[2])
		else:	
			context['HealthData'][listItems[1]] = listItems[2]
	
	for key, values in context['HealthData'].iteritems():
		# Subject to moderation
		if values > subjectToModerationMin:
			values = str(values) + '*'
		
		Data.append([key  , str(values)])

	Data.append(["",""])
	Data.append(["<b> Shelter Situation</b>", "<b>Information</b>"])
	

	context = {}
	context['Shelter'] =  Shelter.objects.values_list()
	context['ShelterData'] = {}

	for listItems in context['Shelter']:
		if listItems[1] in context['ShelterData']:
			context['ShelterData'][listItems[1]] = context['ShelterData'][listItems[1]] + int(listItems[2])
		else:	
			context['ShelterData'][listItems[1]] = listItems[2]
	
	for key, values in context['ShelterData'].iteritems():
		# Subject to moderation
		if values > subjectToModerationMin:
			values = str(values) + '*'
		
		Data.append([key  , str(values)])	



	context['countIMG'] = Files.objects.filter(Type='IMG').count()
	context['countVID'] = Files.objects.filter(Type='VID').count()
	context['countSMS'] = Files.objects.filter(Type='SMS').count()
	context['countTXT'] = Files.objects.filter(Type='TXT').count()
	context['countAUD'] = Files.objects.filter(Type='SVS').count()	

	Data.append(["",""])
	Data.append(["<b>Types of Files in DropBox</b>","<b>Information</b>"])
	Data.append(["Image Files",str(context['countIMG'])])
	Data.append(["Video Files",str(context['countVID'])])
	Data.append(["Audio Files",str(context['countAUD'])])
	Data.append(["Text Files",str(context['countTXT'])])
	Data.append(["SMS Files",str(context['countSMS'])])

	#TODO: Get this line right instead of just copying it from the docs
	style = TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
	               ('TEXTCOLOR',(1,1),(-2,-2),colors.red),
	               ('VALIGN',(0,0),(0,-1),'TOP'),
	               ('TEXTCOLOR',(0,0),(0,-1),colors.blue),
	               ('FONTSIZE', (0, 1), (-1, 1), 18), 
	               ('TEXTFONT', (0, 1), (-1, 1), 'Times-Bold'),
	               ('ALIGN',(0,-1),(-1,-1),'CENTER'),
	               ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
	               ('TEXTCOLOR',(0,-1),(-1,-1),colors.green),
	               ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
	               ('BOX', (0,0), (-1,-1), 0.25, colors.black),
	               ])

	elements.append(Paragraph('<b>* - Subject to Moderation </b>',h2))

	#Configure style and word wrap
	s = getSampleStyleSheet()
	s = s["BodyText"]
	s.wordWrap = 'CJK'
	Data2 = [[Paragraph(cell, s) for cell in row] for row in Data]
	
	t=Table(Data2)

	t.setStyle(style)

	#Send the data and build the file
	elements.append(t)
	
	
	doc.build(elements)
	return response
