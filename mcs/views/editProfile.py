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
		display_type = request.POST.get("delUser", None)
		SMSRegistration.objects.filter(Phone=context['phone']).delete()
		return HttpResponseRedirect("/sms")

	return render(request, 'mcs/editProfile.html', context)
