"""
:Created: 5 May 2015
:Author: Lucas Connors

"""

from django.db import models

from menu.models import MenuItem
from restaurant.models import Table


class Order(models.Model):

    table = models.ForeignKey(Table)
    created = models.DateTimeField(auto_now_add=True)
    completed = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return "Order from table {table}".format(table=self.table)

    def encodeJSON(self):
        return {
            'id': self.id,
            'table': self.table.number,
            'items': [ordermenuitem.encodeJSON() for ordermenuitem in self.ordermenuitem_set.all()],
        }


class OrderMenuItem(models.Model):

    order = models.ForeignKey(Order)
    menuitem = models.ForeignKey(MenuItem)
    quantity = models.PositiveSmallIntegerField(default=1)
    note = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return "{menuitem} from {order}".format(menuitem=self.menuitem, order=self.order)

    def encodeJSON(self):
        return {
            'quantity': self.quantity,
            'name': self.menuitem.name,
            'note': self.note,
        }
