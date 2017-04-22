from django.conf import settings
from django.db import models
from django.utils import timezone

# Models for Shopping List (currently served from external JSON):

class ShoppingList(models.Model):

	class Meta:
#		managed = False		# No database table creation or deletion operations \
							# will be performed for this model. 
		ordering = ['name']

	name = 			models.CharField(db_index=True, unique=False, max_length=40)
#	desc = 			models.TextField(db_index=False, blank=True, null=True)
	unit_price = 	models.DecimalField(max_digits=8, decimal_places=2, db_index=True)
	special_qty = 	models.IntegerField(db_index=True, unique=False, null=False, default=0)
	special_price = models.DecimalField(max_digits=8, decimal_places=2, null=False, default=0)

#metadata:
	created_date = models.DateTimeField(default=timezone.now)
	modified_date = models.DateTimeField(auto_now=True)

	def __str__(self):
		return "%s ($%s)" % (self.name, self.unit_price)

	@property
	def special(self):
		if(special_qty>0 and special_price>0):
			return "%s for $%s" % (self.special_qty, self.special_price)
		else:
			return ""
