"""
:Created: 5 May 2015
:Author: Lucas Connors

"""

from django.db import models


class Table(models.Model):

    number = models.CharField(max_length=60)

    def __str__(self):
        return self.number
