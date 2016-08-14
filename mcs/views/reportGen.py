from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, landscape, portrait
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from  reportlab.lib.styles import ParagraphStyle as PS
from  reportlab.platypus import PageBreak
from  reportlab.platypus.paragraph import Paragraph
from  reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from  reportlab.platypus.tableofcontents import TableOfContents
from  reportlab.platypus.frames import Frame
from  reportlab.lib.units import cm
from django.template import RequestContext
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from django.http import HttpResponse	
from mcs.models import *

def reportGen(request):
	response = HttpResponse(content_type='application/pdf')
	#response['Content-Disposition'] = 'attachement; filename=acs.pdf'
	doc = SimpleDocTemplate(response, pagesize=A4, rightMargin=30,leftMargin=30, topMargin=30,bottomMargin=18)
	doc.pagesize = portrait(A4)

	

	h1 = PS(
			name = 'Heading1',
			fontSize = 14,
			leading = 30,
			leftIndent = 170)
	
	h2 = PS(
			name = 'Heading1',
			fontSize = 12,
			leading = 20,
			leftIndent = 30,
			spaceAfter = 20)

	# Table Headers
	elements = []
	elements.append(Paragraph('<b>Damage Assessment Format</b>', h1))
	elements.append(Paragraph('<i>[In-depth sectoral Assessment to have medium and long-term relief, rehabilitation and reconstruction assistance for critical sectors, assessment to be carried out by specialist]</i>',h2))


	
	context = {}
	context['Food'] =  Food.objects.values_list()
	context['FoodData'] = {}

	for listItems in context['Food']:
		if listItems[1] in context['FoodData']:
			context['FoodData'][listItems[1]] = context['FoodData'][listItems[1]] + int(listItems[2])
		else:	
			context['FoodData'][listItems[1]] = listItems[2]

	Data = [
		["<b>Food Type Requirement</b>", "<b>Information</b>", ],
	]
	
	for key, values in context['FoodData'].iteritems():
		Data.append([key  , str(values)])

	Data.append(["",""])
	Data.append(["<b>Victim Affected</b>", "<b>Information</b>"])
	
	context = {}
	context['Victim'] =  Victims.objects.values_list()
	context['VictimData'] = {}

	for listItems in context['Victim']:
		if listItems[1] in context['VictimData']:
			context['VictimData'][listItems[1]] = context['VictimData'][listItems[1]] + int(listItems[2])
		else:	
			context['VictimData'][listItems[1]] = listItems[2]
	
	for key, values in context['VictimData'].iteritems():
		Data.append([key  , str(values)])

	Data.append(["",""])
	Data.append(["<b> Health Situation</b>", "<b>Information</b>"])
	
	context = {}
	context['Health'] =  Health.objects.values_list()
	context['HealthData'] = {}

	for listItems in context['Health']:
		if listItems[1] in context['HealthData']:
			context['HealthData'][listItems[1]] = context['HealthData'][listItems[1]] + int(listItems[2])
		else:	
			context['HealthData'][listItems[1]] = listItems[2]
	
	for key, values in context['HealthData'].iteritems():
		Data.append([key  , str(values)])

	Data.append(["",""])
	Data.append(["<b> Shelter Situation</b>", "<b>Information</b>"])
	

	context = {}
	context['Shelter'] =  Shelter.objects.values_list()
	context['ShelterData'] = {}

	for listItems in context['Shelter']:
		if listItems[1] in context['ShelterData']:
			context['ShelterData'][listItems[1]] = context['ShelterData'][listItems[1]] + int(listItems[2])
		else:	
			context['ShelterData'][listItems[1]] = listItems[2]
	
	for key, values in context['ShelterData'].iteritems():
		Data.append([key  , str(values)])	



	context['countIMG'] = Files.objects.filter(Type='IMG').count()
	context['countVID'] = Files.objects.filter(Type='VID').count()
	context['countSMS'] = Files.objects.filter(Type='SMS').count()
	context['countTXT'] = Files.objects.filter(Type='TXT').count()
	context['countAUD'] = Files.objects.filter(Type='AUD').count()	

	Data.append(["",""])
	Data.append(["<b>Types of Files in DropBox</b>","<b>Information</b>"])
	Data.append(["Image Files",str(context['countIMG'])])
	Data.append(["Video Files",str(context['countVID'])])
	Data.append(["Audio Files",str(context['countAUD'])])
	Data.append(["Text Files",str(context['countTXT'])])
	Data.append(["SMS Files",str(context['countSMS'])])

	#TODO: Get this line right instead of just copying it from the docs
	style = TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
	               ('TEXTCOLOR',(1,1),(-2,-2),colors.red),
	               ('VALIGN',(0,0),(0,-1),'TOP'),
	               ('TEXTCOLOR',(0,0),(0,-1),colors.blue),
	               ('FONTSIZE', (0, 1), (-1, 1), 18), 
	               ('TEXTFONT', (0, 1), (-1, 1), 'Times-Bold'),
	               ('ALIGN',(0,-1),(-1,-1),'CENTER'),
	               ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
	               ('TEXTCOLOR',(0,-1),(-1,-1),colors.green),
	               ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
	               ('BOX', (0,0), (-1,-1), 0.25, colors.black),
	               ])

	#Configure style and word wrap
	s = getSampleStyleSheet()
	s = s["BodyText"]
	s.wordWrap = 'CJK'
	Data2 = [[Paragraph(cell, s) for cell in row] for row in Data]
	
	t=Table(Data2)

	t.setStyle(style)
	

	#Send the data and build the file
	elements.append(t)
	
	
	doc.build(elements)
	return response
