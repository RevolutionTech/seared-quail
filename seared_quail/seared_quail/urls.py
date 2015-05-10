"""
:Created: 5 May 2015
:Author: Lucas Connors

"""

from django.conf.urls import patterns, include, url
from django.contrib import admin

from menu.views import MenuView
from order.views import KitchenView


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', MenuView.as_view(), name='menu'),
    url(r'^kitchen/?$', KitchenView.as_view(), name='kitchen'),
)
