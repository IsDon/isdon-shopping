from django.contrib import admin

from .models import ShoppingList
# Register your models here.

#if shoppinglist stored in database, add this model to admin site:
admin.site.register(ShoppingList)