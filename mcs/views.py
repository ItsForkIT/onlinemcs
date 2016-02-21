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
                  DateTime=FileInfo['datetime'])
        f.save()
        if(insertToSpecificTable(filePath, FileInfo['type'], f)):
            return 1
    return 0

# Create your views here.


def index(request):
    context = {}
    context['countAllFiles'] = Files.objects.all().count()
    context['countIMG'] = Files.objects.filter(Type='IMG').count()
    context['countVID'] = Files.objects.filter(Type='VID').count()
    context['countSMS'] = Files.objects.filter(Type='SMS').count()
    context['countTXT'] = Files.objects.filter(Type='TXT').count()
    context['countAUD'] = Files.objects.filter(Type='AUD').count()

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
    context['years'] = list()
    for years in context['DateTime']:
        val1 = str(years)
        print(val1)
        context['years'].append(val1[:4])

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

        context['countYears'] = {
            i: context['years'].count(i) for i in context['years']}
        print(context['countYears'])

    return render(request, 'mcs/graphical.html', context)


def tabularAnalysis(request):
    return render(request, 'mcs/tables.html', {})


def imageView(request):
    context = {}
    context['imgList'] = Files.objects.filter(Type='IMG')
    return render(request, 'mcs/images.html', context)


def videoView(request):
    context = {}
    context['vidList'] = Files.objects.filter(Type='VID')
    print(context['vidList'])
    return render(request, 'mcs/videos.html', context)
