from django.shortcuts import render
from mcs.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import shutil,json
from collections import Counter
from django.http import HttpResponse	

def imageView(request):
	image_list = Files.objects.filter(Type='IMG').order_by('-DateTime')
	paginator = Paginator(image_list, 10) # Show 25 contacts per page

	page = request.GET.get('page')
	try:
	    images = paginator.page(page)
	except PageNotAnInteger:
	    # If page is not an integer, deliver first page.
	    images = paginator.page(1)
	except EmptyPage:
		images = paginator.page(paginator.num_pages)
	return render(request, 'mcs/images.html', {'images': images})

def audioView(request):
	context = {}
	context['audioList'] = Files.objects.filter(Type='SVS')
	return render(request, 'mcs/audios.html', context)

def videoView(request):
	context = {}
	context['vidList'] = Files.objects.filter(Type='VID').order_by('-DateTime')
	
	return render(request, 'mcs/videos.html', context)

def groupView(request):
	context = {}
	context['allSource'] = Files.objects.values_list('Source', flat=True).distinct()
	context['groups'] = Files.objects.values_list('GroupId', flat=True).distinct()
	context['groupFin'] = {}
	
	context['checker'] = {}
	
	# checking for RESPONSE
	if request.GET:
		source = request.GET.get('value')
		group = request.GET.get('group')

		context['checker'] = list(Files.objects.filter(Source=source).filter(GroupId=group))

		listGroup = []

		for item in context['checker']:
			listGroup.append(str(item))

		
		data = json.dumps(listGroup)
		
		return HttpResponse(data, "application/json")

	return render(request, 'mcs/group.html', context)
		