from django.conf.urls import include, url
from . import views

urlpatterns = [
	# base url
    url(r'^$', views.latest, name='cart_home'),
    url(r'^latest/$', views.latest, name='cart_latest'),


	# AJAX API:
	url(r'^add/(?P<id>[0-9]+)/(?P<amount>[0-9]+)/$', views.add, name='cart_add'),
	url(r'^remove/(?P<id>[0-9]+)/$', views.remove, name='cart_removeItem'),
]