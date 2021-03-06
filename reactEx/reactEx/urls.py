"""reactEx URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.sites.models import Site

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),


    # Shopping List Views:
    url(r'^shopping/', include('shoppinglist.urls')),

    # Shopping Cart Views:
    url(r'^cart/', include('cart.urls')),



    # AJAX functions:



    # django.js includes:
    url(r'^djangojs/', include('djangojs.urls')),

    # admin site (DJango):
    url(r'^admin/', admin.site.urls),

    # insert userena overrides here as required:

    # base userena:
    url(r'^accounts/', include('userena.urls')),
]

#windows environment static server:
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()

admin.autodiscover()
admin.site.unregister(Site)