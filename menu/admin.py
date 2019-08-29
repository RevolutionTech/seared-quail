"""
:Created: 5 May 2015
:Author: Lucas Connors

"""

from django import forms
from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from menu.models import Category, MenuItem


class CategoryAdmin(OrderedModelAdmin):
    list_display = ('name', 'parent', 'move_up_down_links',)


class MenuItemAdminForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(MenuItemAdminForm, self).clean()

        if not self.errors:
            # user_can_order and not show_in_menu is not allowed
            if not cleaned_data['show_in_menu'] and cleaned_data['user_can_order']:
                raise forms.ValidationError("User cannot order menu items not shown on the menu.")

        return cleaned_data


class MenuItemAdmin(OrderedModelAdmin):
    form = MenuItemAdminForm
    list_display = ('name', 'category', 'show_in_menu', 'user_can_order', 'move_up_down_links',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
