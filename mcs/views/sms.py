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
		if not os.system("ls -l"):
			smsSave = SaveSMS(Destination=request.GET.get('name'), Designation=request.GET.get('designation'), DateTime=timezone.localtime(timezone.now()))
			smsSave.save()

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
