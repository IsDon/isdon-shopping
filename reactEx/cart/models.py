from django.db import models
from django.utils import timezone
from django.db.models import F, Value, Case, When

from django.contrib.auth.models import User
from shoppinglist.models import ShoppingList

# Create your models here.

class Cart(models.Model):

	class Meta:
		get_latest_by = "modified_date"

	user = models.ForeignKey( User, 
		db_index=True,
        related_name="User_Cart",
        related_query_name="User_Carts",
        null=True,
        on_delete=models.CASCADE)

	@property
	def id_hash(self):		# used for user bookmark / saved (or emailed) links of carts
		return self.id ^ 0xABCDEFAB

#history data:
	created_date = models.DateTimeField(default=timezone.now)
	modified_date = models.DateTimeField(auto_now=True)			#last modified, user = latest cart



class CartItemManager(models.Manager):
    """QuerySet manager for class to add non-database fields.

    A @property in the model cannot be used because QuerySets (eg. return
    value from .all()) are directly tied to the database Fields -
    this does not include @property attributes."""

    def get_queryset(self):
        """Overrides the models.Manager method"""
        qs = super(CartItemManager, self).get_queryset().annotate(
           	qu_price=Case(
           		When(item__special_qty__gt=0, then=
					models.ExpressionWrapper(
		           		F('item__unit_price') * (F('quantity') % F('item__special_qty'))
		           		+ F('item__special_price') * (F('quantity') / F('item__special_qty')), 
		        		output_field=models.DecimalField(decimal_places=2)
		        	)
           		),
           		default=models.ExpressionWrapper(
		           		F('item__unit_price') * F('quantity'), 
		        		output_field=models.DecimalField(decimal_places=2)
		        	)
           		#, output_field=models.DecimalField(decimal_places=2)
           	)

	           	
        )
        return qs

class CartItem(models.Model):

	class Meta:
		ordering = ['item__name']

	cart = models.ForeignKey( Cart,
		db_index=True,
		null=False,
		on_delete=models.CASCADE)

	item = models.ForeignKey( ShoppingList,
		db_index=False,
		null=False,
		on_delete=models.CASCADE)

	quantity = models.IntegerField(db_index=False, null=False, default=1)

	@property
	def quantity_price(self):
		return self.item__unit_price * self.quantity

	objects = CartItemManager();