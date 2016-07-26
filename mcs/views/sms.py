from django.shortcuts import render
from mcs.models import *
import shutil,json
from django.http import HttpResponse	

def sms(request):
	context = {}
	context['registeredUserList'] = SMSRegistration.objects.values_list('Name','Designation','Phone')
	
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
