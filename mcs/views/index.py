from django.shortcuts import render
from mcs.models import *
import glob
from os import path
from django.shortcuts import redirect

RELATIVE_PATH_TO_SYNC = "../dms/sync/*"

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

		messageLineSplit = message.split('\n')
		for mesg in messageLineSplit:
			messageSplit = mesg.split(':')

			if(messageSplit[0] == 'Health'):
				strTxtObj = Health(Type=messageSplit[1],Quantity=messageSplit[2],File=fileModelObj)
				strTxtObj.save()
			if(messageSplit[0] == 'Shelter'):
				strTxtObj = Shelter(Type=messageSplit[1],Quantity=messageSplit[2], File=fileModelObj)
				strTxtObj.save()    	
			
			if(messageSplit[0] == 'Victim'):
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
	fileInfo['source'] = info[3]
	fileInfo['destination'] = info[4]
	fileInfo['lat'] = info[5]
	fileInfo['long'] = info[6]
	fileInfo['datetime'] = datetime.strptime(info[7], '%Y%m%d%H%M%S')
	fileInfo['groupId'] = info[8].split(".")[0]
	return fileInfo


def checkAndInsert(filePath):
	fileName = path.basename(filePath)
	if(fileName.startswith("Map")):
		return 0
	if(not Files.objects.filter(Name=fileName).exists()):
		FileInfo = extractFileInfo(fileName)
		size = path.getsize(filePath)
		f = Files(Name=fileName, Type=FileInfo['type'], Size=size,
				  Source=FileInfo['source'],
				  Destination=FileInfo['destination'],
				  lon=FileInfo['long'],
				  lat=FileInfo['lat'],
				  DateTime=FileInfo['datetime'], Ttl=FileInfo['ttl'], GroupId = FileInfo['groupId'])
		f.save()
		if(insertToSpecificTable(filePath, FileInfo['type'], f)):
			return 1
	return 0

def fileStruct():
	fileLatLangTable = {}
	fileList = Files.objects.values_list();

# Create your views here
def index(request):
	context = {}
	context['countAllFiles'] = Files.objects.all().count()
	context['countIMG'] = Files.objects.filter(Type='IMG').count()
	context['countVID'] = Files.objects.filter(Type='VID').count()
	context['countSMS'] = Files.objects.filter(Type='SMS').count()
	context['countTXT'] = Files.objects.filter(Type='TXT').count()
	context['countAUD'] = Files.objects.filter(Type='AUD').count()
	allFiles = Files.objects.all()
	context['latlong'] = [(i.lat, i.lon, i.Name) for i in allFiles]
	sum = 0
	sum1 = 0
	for pair in context['latlong']:
   		sum += pair[0]
   		sum1 += pair[1]

	if context['countAllFiles'] > 0:
   		print context['latlong']
	   	context['latlongAvg'] = (sum/context['countAllFiles'],sum1/context['countAllFiles'])
	   	print context['latlongAvg']
	else:
		context['latlongAvg'] = (23.548822,87.29262)   	
   	
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

