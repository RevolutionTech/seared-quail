"""
:Created: 5 May 2015
:Author: Lucas Connors

"""

from django.db import models

from menu.models import MenuItem
from restaurant.models import Table


class Order(models.Model):

    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    completed = models.DateTimeField(null=True, blank=True)

    def encodeJSON(self):
        return {
            "id": self.id,
            "table": self.table.number,
            "items": [
                ordermenuitem.encodeJSON()
                for ordermenuitem in self.ordermenuitem_set.all()
            ],
        }


class OrderMenuItem(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)
    note = models.TextField(null=True, blank=True)

    def encodeJSON(self):
        return {
            "quantity": self.quantity,
            "name": self.menuitem.name,
            "note": self.note,
        }
