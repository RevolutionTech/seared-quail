"""
:Created: 6 May 2015
:Author: Lucas Connors

"""

from django import forms

from menu.models import MenuItem
from restaurant.models import Table


class MenuForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(MenuForm, self).__init__(*args, **kwargs)

        # Create a field for each menu item
        for menuitem in MenuItem.objects.all():
            self.fields['quantity-{id_}'.format(id_=menuitem.id)] = forms.IntegerField(min_value=0)

    table = forms.IntegerField()

    def clean_table(self):
        tableid = self.cleaned_data['table']
        try:
            table = Table.objects.get(id=tableid)
        except Table.DoesNotExist:
            raise forms.ValidationError("Given table does not exist.")
        return table

    def clean(self):
        cleaned_data = super(MenuForm, self).clean()

        if not self.errors:
            # Collapse menu items into single key
            menuitems = []
            for label, quantity in cleaned_data.items():
                if label.startswith('quantity-'):
                    if quantity > 0:
                        menuitemid = int(label.split('-')[1])
                        menuitem = MenuItem.objects.get(id=menuitemid)
                        menuitems.append({
                            'menuitem': menuitem,
                            'quantity': quantity,
                        })
                    del cleaned_data[label]
            cleaned_data['menuitems'] = menuitems

        return cleaned_data
