"""
:Created: 5 May 2015
:Author: Lucas Connors

"""

from django.core.exceptions import ValidationError
from django.db import models
from ordered_model.models import OrderedModel


class Category(OrderedModel):

    name = models.CharField(max_length=30)
    parent = models.ForeignKey('self', null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    order_with_respect_to = 'parent'

    class Meta(OrderedModel.Meta):
        verbose_name_plural = "Categories"

    def __unicode__(self):
        return self.name

    def clean(self):
        self.check_ancestor_of_self()
        return super(Category, self).clean()

    def check_ancestor_of_self(self):
        parent = self.parent
        while parent is not None:
            if parent == self:
                raise ValidationError({'parent': "Category may not be an ancestor subcategory of itself."})
            else:
                parent = parent.parent


class MenuItem(OrderedModel):

    category = models.ForeignKey(Category)
    name = models.CharField(max_length=30)
    img = models.ImageField(upload_to="img/menuitem", null=True, blank=True, verbose_name='Image')
    description = models.TextField(null=True, blank=True)
    enabled = models.BooleanField(default=True)

    order_with_respect_to = 'category'

    class Meta(OrderedModel.Meta):
        pass

    def __unicode__(self):
        return self.name
