"""
:Created: 5 May 2015
:Author: Lucas Connors

"""

from django.contrib import admin
from django.utils.html import format_html
from ordered_model.admin import OrderedModelAdmin

from menu.models import Category, MenuItem


class MenuItemAdmin(OrderedModelAdmin):
    list_display = ('name', 'category', 'enabled', 'move_up_down_links',)


admin.site.register(Category)
admin.site.register(MenuItem, MenuItemAdmin)
