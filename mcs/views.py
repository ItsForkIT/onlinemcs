from django.shortcuts import render
from django.shortcuts import redirect
from .models import *
import glob
from os import path
from datetime import datetime

RELATIVE_PATH_TO_SYNC = "../sync/*"


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
    return render(request, 'mcs/index.html', context)


def sync(request):
    allFilePaths = glob.glob(RELATIVE_PATH_TO_SYNC)
    i = 0
    for filePath in allFilePaths:
        i += checkAndInsert(filePath)
    print(str(i) + " Files inserted")
    return redirect(index)


def graphicalAnalysis(request):
    return render(request, 'mcs/graphical.html', {})
