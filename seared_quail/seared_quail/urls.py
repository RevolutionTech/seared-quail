"""
:Created: 5 May 2015
:Author: Lucas Connors

"""

from django.conf.urls import patterns, include, url
from django.contrib import admin

from menu.views import MenuView


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', MenuView.as_view(), name='menu'),
)
