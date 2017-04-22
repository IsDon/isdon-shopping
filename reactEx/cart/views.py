from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from rest_framework.renderers import JSONRenderer
from django.db.models import F, Sum
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from cart.models import Cart, CartItem
from shoppinglist.models import ShoppingList

# Base Views:
@login_required
def home(request):

	response = render(request, 'reactEx/front.html')

	return response

# JSON data with latest cart (default for user)  or cart if passed:
@login_required
def latest(request, cart=None):

	if(cart):
		user_cart = cart
	else:
		user_cart=getUserLatestCart(request.user)

	cart_raw = CartItem.objects.filter(cart=user_cart).annotate(
		id_link=F('item_id')
		).values(
		'id_link', 'id', 'item', 'item__name', 'quantity', 'qu_price'
		)

	cart_filled = list(cart_raw)
	if(cart_filled):
		cart_filled.append({
			'id':-1, 
			'item__name':'TOTAL',
			'qu_price': cart_raw.aggregate(Sum('qu_price'))['qu_price__sum']
		})

	return JsonResponse(cart_filled, safe=False)

# Test build only:

# AJAX views:
@login_required
def add(request, id, amount=1):
	try:
		amount = int(amount)
	except BaseException as e:
		return JsonResponse({'error':'addToCart - amount', 'err_msg':str(e)})

	try:
		item=ShoppingList.objects.get(pk=id)
	except ShoppingList.DoesNotExist as e:
		print('ShoppingList PK not found')
		return JsonResponse({'error':'addToCart', 'err_msg':str(e)})

	user_cart=getUserLatestCart(request.user)

	try:
		cartItem = CartItem.objects.get(cart=user_cart, item=item)
	except CartItem.DoesNotExist as e:
		cartItem = CartItem.objects.create(cart=user_cart, item=item, quantity=0)

	cartItem.quantity = cartItem.quantity + amount
	cartItem.save()

	return latest(request)

def getUserLatestCart(cart_user):

	try:
		user_cart = Cart.objects.filter(user=cart_user).latest()
	except Cart.DoesNotExist as e:
		user_cart = Cart.objects.create(user=cart_user)
	return user_cart


@login_required
@csrf_exempt
def remove(request, id):
	#Remove cart items from user current cart

	try:
		user_cart = Cart.objects.filter(user=request.user).latest()
	except BaseException as e:
		return JsonResponse({'error':'addToCart', 'err_msg':str(e)})

	try:
		item=ShoppingList.objects.get(pk=id)
	except ShoppingList.DoesNotExist as e:
		print('ShoppingList PK not found')
		print(id)
		return JsonResponse({'error':'addToCart', 'err_msg':str(e)})

	CartItem.objects.filter(cart=user_cart, item=item).delete()
	#optimistic, faster option: untested::   Cart.objects.filter(user=request.user, item_id=id).delete()

	return latest(request)