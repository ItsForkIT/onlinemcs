from django.shortcuts import render
from mcs.models import *
import glob
from os import path
from django.shortcuts import redirect
import datetime
import logging
import json

from .utils import manageGis

log = logging.getLogger(__name__)

RELATIVE_PATH_TO_SYNC = "../DMS/sync/*"
RELATIVE_PATH_TO_GIS = "static/geojson/"
RELATIVE_PATH_TO_TARGET_GIS = "static/sampleGeoJson/sample.geojson"


def insertToSpecificTable(filePath, fileType, fileModelObj):
    if(fileType == 'SMS'):
        fileObj = open(filePath, 'r')
        message = str(fileObj.read())
        #sentiment = TextBlob(message).sentiment.polarity
        # uTxtObj = UnstructuredTXT(Content=message, File=fileModelObj,
        #                         SentimentPolarity=sentiment)
        # uTxtObj.save()
        return 1
    if(fileType == 'TXT'):
        fileObj = open(filePath, 'r')
        message = str(fileObj.read())

        messageLineSplit = message.split('\n')
        for mesg in messageLineSplit:
            messageSplit = mesg.split(':')

            if(messageSplit[0] == 'Health'):
                strTxtObj = Health(Type=messageSplit[1], Quantity=messageSplit[
                                   2], File=fileModelObj)
                strTxtObj.save()
            if(messageSplit[0] == 'Shelter'):
                strTxtObj = Shelter(Type=messageSplit[1],
                                    Quantity=messageSplit[2],
                                    File=fileModelObj)
                strTxtObj.save()

            if(messageSplit[0] == 'Victim'):
                strTxtObj = Victims(Type=messageSplit[1],
                                    Quantity=messageSplit[2],
                                    File=fileModelObj)
                strTxtObj.save()

            if(messageSplit[0] == 'Food'):
                strTxtObj = Food(Type=messageSplit[1], Quantity=messageSplit[
                                 2], File=fileModelObj)
                strTxtObj.save()

            # if(messageSplit[0] == 'Areas'):
            #   strTxtObj = Food(Type=messageSplit[1],Quantity=messageSplit[2], File=fileModelObj)
            #   strTxtObj.save()
    return 1


def extractFileInfo(fileName):
    info = fileName.split("_")
    if len(info) != 9:
        log.error(str(fileName) + "," + "Wrong file structure")
        return 0
    fileInfo = {}
    fileInfo['type'] = info[0]
    fileInfo['ttl'] = info[1]
    fileInfo['source'] = info[3]
    fileInfo['destination'] = info[4]
    fileInfo['lat'] = info[5]
    fileInfo['long'] = info[6]
    fileInfo['datetime'] = datetime.datetime.strptime(info[7], '%Y%m%d%H%M%S')
    fileInfo['groupId'] = info[8].split(".")[0]
    return fileInfo


def checkAndInsert(filePath):
    fileName = path.basename(filePath)
    if(fileName.startswith("Map")):
        return 0
    if(not Files.objects.filter(Name=fileName).exists()):
        FileInfo = extractFileInfo(fileName)
        if FileInfo == 0:
            return 0
        size = path.getsize(filePath)
        f = Files(Name=fileName, Type=FileInfo['type'], Size=size,
                  Source=FileInfo['source'],
                  Destination=FileInfo['destination'],
                  lon=FileInfo['long'],
                  lat=FileInfo['lat'],
                  DateTime=FileInfo['datetime'],
                  Ttl=FileInfo['ttl'],
                  GroupId=FileInfo['groupId'])

        log.info(str(fileName) + "," + "inserted into DB")
        f.save()
        if(insertToSpecificTable(filePath, FileInfo['type'], f)):
            return 1
    return 0


#   test = Files.objects.filter(DateTime__range=(first_date,last_date))

# Create your views here


def index(request):
    context = {}
    context['countAllFiles'] = Files.objects.all().count()
    context['countIMG'] = Files.objects.filter(Type='IMG').count()
    context['countVID'] = Files.objects.filter(Type='VID').count()
    context['countSMS'] = Files.objects.filter(Type='SMS').count()
    context['countTXT'] = Files.objects.filter(Type='TXT').count()
    context['countAUD'] = Files.objects.filter(Type='SVS').count()
    allFiles = Files.objects.all()
    '''
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

    # Increment Counter in timeSlice
    delta = datetime.timedelta(minutes=timeSlice)
    while minFileDateTime <= maxFileDateTime:
        #minFileTime = datetime.datetime.strptime(minFileDateTime,'%Y%m%d%H%M%S')
        #maxFileTime = datetime.datetime.strptime(maxFileDateTime,'%Y%m%d%H%M%S')
        allFilesRange = Files.objects.filter(DateTime__range=(minFileDateTime,maxFileDateTime))
        print allFilesRange
        noOfClusters += 1
        minFileDateTime += delta


    print 'No. of Clusters : ' + str(noOfClusters)
    '''
    context['latlong'] = [(i.lat, i.lon, i.Name.split("_")[2])
                          for i in allFiles]
    sum = 0
    sum1 = 0
    for pair in context['latlong']:
        sum += pair[0]
        sum1 += pair[1]

    if context['countAllFiles'] > 0:
        context['latlongAvg'] = (
            sum / context['countAllFiles'], sum1 / context['countAllFiles'])
    else:
        context['latlongAvg'] = (23.548822, 87.29262)

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
    manageGis(allFilePaths, RELATIVE_PATH_TO_GIS, RELATIVE_PATH_TO_TARGET_GIS)
    return redirect(index)
