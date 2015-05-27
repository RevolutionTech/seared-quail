"""
:Created: 5 May 2015
:Author: Lucas Connors

"""

from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from menu.models import Category, MenuItem


class CategoryAdmin(OrderedModelAdmin):
    list_display = ('name', 'parent', 'move_up_down_links',)


class MenuItemAdmin(OrderedModelAdmin):
    list_display = ('name', 'category', 'enabled', 'move_up_down_links',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
