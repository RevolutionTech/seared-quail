"""
:Created: 5 May 2015
:Author: Lucas Connors

"""

from django.contrib import admin

from menu.models import Category, MenuItem


admin.site.register(Category)
admin.site.register(MenuItem)
