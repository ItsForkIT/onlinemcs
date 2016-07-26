from django.shortcuts import render
from mcs.models import *

def tabularAnalysis(request):
	context = {}
	context['countAllFiles'] = Files.objects.all().count()
	context['countIMG'] = Files.objects.filter(Type='IMG').count()
	context['countVID'] = Files.objects.filter(Type='VID').count()
	context['countSMS'] = Files.objects.filter(Type='SMS').count()
	context['countTXT'] = Files.objects.filter(Type='TXT').count()
	context['countAUD'] = Files.objects.filter(Type='AUD').count()

	context['Ttl'] = Files.objects.values_list('Ttl', flat=True)
	context['TtlVal'] = list()
	for years in context['Ttl']:       
		val1 = str(years) 
		context['TtlVal'].append(val1)
	
	
	context['Health'] =  Health.objects.values_list()
	context['HealthData'] = {}
	for listItems in context['Health']:
		if listItems[1] in context['HealthData']:
			context['HealthData'][listItems[1]] = context['HealthData'][listItems[1]] + int(listItems[2])
		else:	
			context['HealthData'][listItems[1]] = listItems[2]

	context['Food'] =  Food.objects.values_list()

	context['FoodData'] = {}

	for listItems in context['Food']:
		if listItems[1] in context['FoodData']:
			context['FoodData'][listItems[1]] = context['FoodData'][listItems[1]] + int(listItems[2])
		else:	
			context['FoodData'][listItems[1]] = listItems[2]


	context['Victims'] = Victims.objects.values_list()
	context['VictimsCount'] = Victims.objects.all().count()
	context['VictimData'] = {}
	context['VictimDataPerc'] = {}

	for listItems in context['Victims']:
		if listItems[1] in context['VictimData']:
			context['VictimData'][listItems[1]] = context['VictimData'][listItems[1]] + int(listItems[2])

		else:	
			context['VictimData'][listItems[1]] = listItems[2]

	print context['VictimData']
	context['TtlFinalVal'] = {j:context['TtlVal'].count(j) for j in context['TtlVal']}
   
	return render(request, 'mcs/tables.html', context)
