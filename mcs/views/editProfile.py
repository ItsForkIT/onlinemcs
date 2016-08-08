from django.shortcuts import render, redirect
from mcs.models import *
from django.http import HttpResponseRedirect

def editProfile(request):
	context = {}
	if request.GET:
		context['phone'] = request.GET.get('phone')

		context['name'] = SMSRegistration.objects.get(Phone=context['phone']).Name
		context['email'] = SMSRegistration.objects.get(Phone=context['phone']).Email
		context['designation'] = SMSRegistration.objects.get(Phone=context['phone']).Designation

	if request.method == "POST":
		if 'delUser' in request.POST:
			display_type = request.POST.get("delUser", None)
			SMSRegistration.objects.filter(Phone=context['phone']).delete()
			return HttpResponseRedirect("/sms")
		if 'editUser' in request.POST:
			name = request.POST.get('Name')
			email = request.POST.get('Email')
			phone = request.POST.get('Phone')
			designation = request.POST.get('Designation')
			print name + email + phone + designation
			#form = SMSRegistration(Name=name, Email=email, Phone=phone, Designation = designation)
			#form.save()
			findMatchedData = SMSRegistration.objects.get(Phone=context['phone'])
			findMatchedData.Name = name
			findMatchedData.Email = email
			findMatchedData.Phone = phone
			findMatchedData.Designation = designation

			findMatchedData.save()

			return HttpResponseRedirect("/sms")

	return render(request, 'mcs/editProfile.html', context)
