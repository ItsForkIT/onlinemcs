from django.shortcuts import render, redirect
from mcs.models import *
from django.http import HttpResponseRedirect

def missing(request):
	context = {}
	return render(request, 'mcs/missing.html', context)
