from django.conf.urls import include, url
from . import views

urlpatterns = [
	# base url
    url(r'^$', views.home, name='list_home'),


	# AJAX API:
	url(r'^update/$', views.update, name='list_update'),
]