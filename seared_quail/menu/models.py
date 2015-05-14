"""
:Created: 5 May 2015
:Author: Lucas Connors

"""

from django.db import models


class Category(models.Model):

    name = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.name


class MenuItem(models.Model):

    category = models.ForeignKey(Category)
    name = models.CharField(max_length=30)
    img = models.ImageField(upload_to="img/menuitem", null=True, blank=True, verbose_name='Image')
    description = models.TextField(null=True, blank=True)
    enabled = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name
