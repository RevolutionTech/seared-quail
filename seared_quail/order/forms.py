"""
:Created: 10 May 2015
:Author: Lucas Connors

"""

from django import forms

from order.models import Order


class OrderCompleteForm(forms.Form):

    order = forms.IntegerField(min_value=1)

    def clean_order(self):
        orderid = self.cleaned_data['order']
        try:
            order = Order.objects.get(id=orderid)
        except Order.DoesNotExist:
            raise forms.ValidationError("Given order does not exist.")
        return order
