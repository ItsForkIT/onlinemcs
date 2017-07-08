from django.shortcuts import render
from mcs.models import *

def twitter(request):
	context = {}
	return render(request, 'mcs/twitter.html', context)

