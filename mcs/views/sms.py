from django.shortcuts import render
from mcs.models import *
import shutil,json
from django.http import HttpResponse	
import os, datetime
from django.utils import timezone

def sms(request):
	context = {}
	context['registeredUserList'] = SMSRegistration.objects.values_list('Name','Designation','Phone')
	context['sentSMS'] = SaveSMS.objects.values_list('Destination','Designation','DateTime').order_by('-DateTime')
	
	if request.GET:
		source = request.GET.get('sms')
		SMSString = "SMS From OfflineMCS Software\n"
		
		context = {}	
		context['Food'] =  Food.objects.values_list()
		context['FoodData'] = {}

		for listItems in context['Food']:
			if listItems[1] in context['FoodData']:
				context['FoodData'][listItems[1]] = context['FoodData'][listItems[1]] + int(listItems[2])
			else:	
				context['FoodData'][listItems[1]] = listItems[2]

		
		for key, values in context['FoodData'].iteritems():
			SMSString = SMSString + str(key) + ':' + str(values) + "\n"

	
		context = {}
		context['Victim'] =  Victims.objects.values_list()
		context['VictimData'] = {}

		for listItems in context['Victim']:
			if listItems[1] in context['VictimData']:
				context['VictimData'][listItems[1]] = context['VictimData'][listItems[1]] + int(listItems[2])
			else:	
				context['VictimData'][listItems[1]] = listItems[2]

		for key, values in context['VictimData'].iteritems():
			SMSString = SMSString + str(key) + ':' + str(values) + "\n"

		context = {}
		context['Health'] =  Health.objects.values_list()
		context['HealthData'] = {}

		for listItems in context['Health']:
			if listItems[1] in context['HealthData']:
				context['HealthData'][listItems[1]] = context['HealthData'][listItems[1]] + int(listItems[2])
			else:	
				context['HealthData'][listItems[1]] = listItems[2]

		for key, values in context['HealthData'].iteritems():
			SMSString = SMSString + str(key) + ':' + str(values) + "\n"

		print SMSString	

		#if not os.system("ls -l"):
		#	smsSave = SaveSMS(Destination=request.GET.get('name'), Designation=request.GET.get('designation'), DateTime=timezone.localtime(timezone.now()))
		#	smsSave.save()

			# Create string to Send SMS

		#                os.system("gammu sendsms TEXT " + source + " -text " + "'Halooo ...'")
	
	if request.method == 'POST':
		name = request.POST.get('Name')
		email = request.POST.get('Email')
		phone = request.POST.get('Phone')
		designation = request.POST.get('Designation')

		form = SMSRegistration(Name=name, Email=email, Phone=phone, Designation = designation)
		form.save()

		return render(request, 'mcs/sms.html', context)
	else:
		form = ""
	return render(request, 'mcs/sms.html', context)
