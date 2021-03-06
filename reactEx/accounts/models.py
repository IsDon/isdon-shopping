from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save #, pre_delete
from django.utils import timezone

from django.contrib.auth.models import User
from userena.models import UserenaBaseProfile

# profile extends (one to one) Django User model. 
# TIP: Use User.objects...select_related('profile') where need both data
class Profile(UserenaBaseProfile):
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	location = models.CharField(max_length=30, blank=True)
	birth_date = models.DateField(null=True, blank=True)

# Contact Info:
	
#metadata:
	created_date = models.DateTimeField(default=timezone.now)
	modified_date = models.DateTimeField(auto_now=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])

#user preferences or other additional per-user models:
#	shopping history, search prefs...