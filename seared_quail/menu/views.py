"""
:Created: 5 May 2015
:Author: Lucas Connors

"""

from django.views.generic import TemplateView

from menu.models import Category
from restaurant.models import Table


class MenuView(TemplateView):

    template_name = 'menu.html'

    def get_context_data(self, **kwargs):
        context = super(MenuView, self).get_context_data(**kwargs)

        menu = []
        for category in Category.objects.all():
            if category.menuitem_set.exists():
                menu.append({
                    'name': category.name,
                    'description': category.description,
                    'menuitems': category.menuitem_set.all(),
                })
        context['menu'] = menu
        context['tables'] = Table.objects.all()

        return context
