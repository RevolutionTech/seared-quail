"""
:Created: 5 May 2015
:Author: Lucas Connors

"""

from django.contrib import admin
from django.utils.html import format_html
from ordered_model.admin import OrderedModelAdmin

from menu.models import Category, MenuItem


class MenuItemAdmin(OrderedModelAdmin):
    list_display = ('move_up_down_links', 'menu_item', 'enabled',)

    def menu_item(self, obj):
        return format_html("<a href=\"{id}/\">{name}</a>", id=obj.id, name=obj.name)
    menu_item.allow_tags = True


admin.site.register(Category)
admin.site.register(MenuItem, MenuItemAdmin)
