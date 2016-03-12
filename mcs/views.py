from django.shortcuts import render
from django.shortcuts import redirect
from .models import *
import glob
from os import path
from datetime import datetime
from textblob import TextBlob

RELATIVE_PATH_TO_SYNC = "../sync/*"


def insertToSpecificTable(filePath, fileType, fileModelObj):
	if(fileType == 'SMS'):
		fileObj = open(filePath, 'r')
		message = str(fileObj.read())
		sentiment = TextBlob(message).sentiment.polarity
		uTxtObj = UnstructuredTXT(Content=message, File=fileModelObj,
								  SentimentPolarity=sentiment)
		uTxtObj.save()
		return 1
	if(fileType == 'TXT'):
		fileObj = open(filePath, 'r')
		message = str(fileObj.read())
		messageSplit = message.split(':')

		if(messageSplit[0] == 'Health'):
			strTxtObj = Health(Type=messageSplit[1],Quantity=messageSplit[2],File=fileModelObj)
			strTxtObj.save()
		if(messageSplit[0] == 'Shelter'):
			strTxtObj = Shelter(Type=messageSplit[1],Quantity=messageSplit[2], File=fileModelObj)
			strTxtObj.save()    	
		
		if(messageSplit[0] == 'Victims'):
			strTxtObj = Victims(Type=messageSplit[1],Quantity=messageSplit[2], File=fileModelObj)
			strTxtObj.save()    	
		
		if(messageSplit[0] == 'Food'):
			strTxtObj = Food(Type=messageSplit[1],Quantity=messageSplit[2], File=fileModelObj)
			strTxtObj.save()
		
		if(messageSplit[0] == 'Areas'):
			strTxtObj = Food(Type=messageSplit[1],Quantity=messageSplit[2], File=fileModelObj)
			strTxtObj.save()
		
	return 1


def extractFileInfo(fileName):
	info = fileName.split("_")
	fileInfo = {}
	fileInfo['type'] = info[0]
	fileInfo['ttl'] = info[1]
	fileInfo['source'] = info[2]
	fileInfo['destination'] = info[3]
	fileInfo['lat'] = info[4]
	fileInfo['long'] = info[5]
	fileInfo['datetime'] = datetime.strptime(info[6], '%Y%m%d%H%M%S')
	fileInfo['groupId'] = info[7].split(".")[0]
	return fileInfo


def checkAndInsert(filePath):
	fileName = path.basename(filePath)
	if(not Files.objects.filter(Name=fileName).exists()):
		FileInfo = extractFileInfo(fileName)
		size = path.getsize(filePath)
		f = Files(Name=fileName, Type=FileInfo['type'], Size=size,
				  Source=FileInfo['source'],
				  Destination=FileInfo['destination'],
				  lon=FileInfo['long'],
				  lat=FileInfo['lat'],
				  DateTime=FileInfo['datetime'], Ttl=FileInfo['ttl'])
		f.save()
		if(insertToSpecificTable(filePath, FileInfo['type'], f)):
			return 1
	return 0

def fileStruct():
	fileLatLangTable = {}
	fileList = Files.objects.values_list();
	for item in fileList:
		print 

# Create your views here
def index(request):
	fileStruct()
	context = {}
	context['countAllFiles'] = Files.objects.all().count()
	context['countIMG'] = Files.objects.filter(Type='IMG').count()
	context['countVID'] = Files.objects.filter(Type='VID').count()
	context['countSMS'] = Files.objects.filter(Type='SMS').count()
	context['countTXT'] = Files.objects.filter(Type='TXT').count()
	context['countAUD'] = Files.objects.filter(Type='AUD').count()
	allFiles = Files.objects.all()
	context['latlong'] = [(i.lat, i.lon) for i in allFiles]
	
	if context['countAllFiles'] > 0:
		context['audioDistribution'] = (
			context['countAUD'] * 100) / context['countAllFiles']
		context['smsDistribution'] = (
			context['countSMS'] * 100) / context['countAllFiles']
		context['imageDistribution'] = (
			context['countIMG'] * 100) / context['countAllFiles']
		context['txtDistribution'] = (
			context['countTXT'] * 100) / context['countAllFiles']
		context['videoDistribution'] = (
			context['countVID'] * 100) / context['countAllFiles']

	context['listIMG'] = Files.objects.filter(Type='IMG')
	return render(request, 'mcs/index.html', context)

def sync(request):
	allFilePaths = glob.glob(RELATIVE_PATH_TO_SYNC)
	i = 0
	for filePath in allFilePaths:
		i += checkAndInsert(filePath)
	print(str(i) + " Files inserted")
	return redirect(index)


def graphicalAnalysis(request):
	context = {}
	context['countAllFiles'] = Files.objects.all().count()
	context['countIMG'] = Files.objects.filter(Type='IMG').count()
	context['countVID'] = Files.objects.filter(Type='VID').count()
	context['countSMS'] = Files.objects.filter(Type='SMS').count()
	context['countTXT'] = Files.objects.filter(Type='TXT').count()
	context['countAUD'] = Files.objects.filter(Type='AUD').count()
	context['DateTime'] = Files.objects.values_list('DateTime', flat=True)
	
	context['Health'] =  Health.objects.values_list()
	context['HealthData'] = {}
	for x in context['Health']:
		context['HealthData'][x[1]] = x[2]
	print context['HealthData']

	context['Food'] =  Food.objects.values_list()

	context['FoodData'] = {}
	for x in context['Food']:
		context['FoodData'][x[1]] = x[2]
	print context['FoodData']


	context['Victims'] = Victims.objects.values_list()
	context['VictimsCount'] = Victims.objects.all().count()
	print context['Victims']
	context['VictimData'] = {}
	for x in context['Victims']:
		countVictimPerc = (x[2]* 100 / context['VictimsCount'])/2
		context['VictimData'][x[1]] = countVictimPerc

	print context['VictimData']


	context['years'] = list()
	for years in context['DateTime']:
		val1 = str(years)
		
		context['years'].append(val1[:7])

	if context['countAllFiles'] > 0:
		context['audioDistribution'] = ((context['countAUD'] * 100) /
										context['countAllFiles'])
		context['smsDistribution'] = ((context['countSMS'] * 100) /
									  context['countAllFiles'])
		context['imageDistribution'] = ((context['countIMG'] * 100) /
										context['countAllFiles'])
		context['txtDistribution'] = ((context['countTXT'] * 100) /
									  context['countAllFiles'])
		context['videoDistribution'] = ((context['countVID'] * 100) /
										context['countAllFiles'])

		context['countYears'] = {i:context['years'].count(i) for i in context['years']}
		print(context['countYears'])

	return render(request, 'mcs/graphical.html', context)

def tabularAnalysis(request):
	context = {}
	context['countAllFiles'] = Files.objects.all().count()
	context['countIMG'] = Files.objects.filter(Type='IMG').count()
	context['countVID'] = Files.objects.filter(Type='VID').count()
	context['countSMS'] = Files.objects.filter(Type='SMS').count()
	context['countTXT'] = Files.objects.filter(Type='TXT').count()
	context['countAUD'] = Files.objects.filter(Type='AUD').count()

	context['Ttl'] = Files.objects.values_list('Ttl', flat=True)
	context['TtlVal'] = list()
	for years in context['Ttl']:       
		val1 = str(years) 
		context['TtlVal'].append(val1)
	
	
	context['Health'] =  Health.objects.values_list()
	context['HealthData'] = {}
	for x in context['Health']:
		context['HealthData'][x[1]] = x[2]
	print context['HealthData']

	context['Food'] =  Food.objects.values_list()

	context['FoodData'] = {}
	for x in context['Food']:
		context['FoodData'][x[1]] = x[2]
	print context['FoodData']


	context['Victims'] = Victims.objects.values_list()
	context['VictimsCount'] = Victims.objects.all().count()
	print context['Victims']
	context['VictimData'] = {}
	for x in context['Victims']:
		countVictimPerc = (x[2])
		context['VictimData'][x[1]] = countVictimPerc

	print context['VictimData']

	
	context['TtlFinalVal'] = {j:context['TtlVal'].count(j) for j in context['TtlVal']}
	print(context['TtlFinalVal'])
   
	return render(request, 'mcs/tables.html', context)

def imageView(request):
	context = {}
	context['imgList'] = Files.objects.filter(Type='IMG')
	
	return render(request, 'mcs/images.html', context)

def videoView(request):
	context = {}
	context['vidList'] = Files.objects.filter(Type='VID')
	print(context['vidList'])
	return render(request, 'mcs/videos.html', context)
