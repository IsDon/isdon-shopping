from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from rest_framework.renderers import JSONRenderer
from django.contrib.auth.decorators import login_required
#from django.core import serializers
import json

from django.views.decorators.csrf import csrf_exempt

from .models import ShoppingList

# Base Views:
@login_required
def home(request):

	response = render(request, 'reactEx/front.html')

	return response

@csrf_exempt
def update(request):

	data = request.POST
	objs = json.loads(request.body.decode('utf-8'))
	#objs = (objs.get('prices'))
	objs = (objs['prices'])
	# objs.pop('csrfmiddlewaretoken')
	# print(objs)

	# update items in ShoppingList on server
	for o in objs:
		record,created = ShoppingList.objects.get_or_create(name=o['name'])
		record.unit_price = o['unit_price']
		if('special_qty' in o):
			record.special_qty = o['special_qty']
			record.special_price = o['special_price']
		record.save()
	
	return JsonResponse(list(ShoppingList.objects.all().values(
		'id', 'name', 'unit_price', 'special_qty', 'special_price'
		)), safe=False)
	#return JsonResponse(objs, safe=False)



	#TODO - store old values with dateAmmended for archival cartdata review

