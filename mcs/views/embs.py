from django.shortcuts import render
from mcs.models import *

def embs(request):
	context = {}
	return render(request, 'mcs/embs.html', context)

