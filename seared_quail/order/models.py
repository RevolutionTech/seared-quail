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

    def __unicode__(self):
        return "Order from table {table}".format(table=self.table)


class OrderMenuItem(models.Model):

    order = models.ForeignKey(Order)
    menuitem = models.ForeignKey(MenuItem)
    quantity = models.PositiveSmallIntegerField(default=1)
    note = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return "{menuitem} from order {order}".format(menuitem=self.menuitem, order=self.order)
