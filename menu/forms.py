"""
:Created: 6 May 2015
:Author: Lucas Connors

"""

from django import forms

from menu.models import MenuItem
from restaurant.models import Table


class MenuForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create a field for each menu item
        for menuitem in MenuItem.objects.filter(user_can_order=True):
            self.fields[f"quantity-{menuitem.id}"] = forms.IntegerField(min_value=0)
            self.fields[f"note-{menuitem.id}"] = forms.CharField(required=False)

    table = forms.IntegerField()

    def clean_table(self):
        tableid = self.cleaned_data["table"]
        try:
            table = Table.objects.get(id=tableid)
        except Table.DoesNotExist:
            raise forms.ValidationError("Given table does not exist.")
        return table

    def check_leftover_menuitems(self, cleaned_data):
        leftover_menuitems = set(self.data.keys()) - set(cleaned_data.keys())
        for label in leftover_menuitems:
            if label.startswith("quantity-"):
                menuitemid = int(label.split("-")[1])
                menuitem = MenuItem.objects.get(id=menuitemid)
                raise forms.ValidationError(
                    "The item {item_name} is no longer available. Please make a different order.".format(
                        item_name=menuitem.name
                    )
                )

    def clean(self):
        cleaned_data = super().clean()

        if not self.errors:
            # Check for menu items that have been removed since the form was loaded
            self.check_leftover_menuitems(cleaned_data)

            # Collapse menu items into single key
            menuitems = []
            for label, value in list(cleaned_data.items()):
                if label.startswith("quantity-"):
                    if value > 0:
                        menuitemid = int(label.split("-")[1])
                        menuitem = MenuItem.objects.get(id=menuitemid)
                        note = cleaned_data[f"note-{menuitemid}"]
                        menuitems.append(
                            {"menuitem": menuitem, "quantity": value, "note": note}
                        )
                    del cleaned_data[label]
            cleaned_data["menuitems"] = menuitems

        return cleaned_data
