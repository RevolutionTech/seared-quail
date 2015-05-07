"""
:Created: 5 May 2015
:Author: Lucas Connors

"""

from django.core.urlresolvers import reverse
from django.views.generic.edit import FormView


from menu.models import Category
from menu.forms import MenuForm
from order.models import Order, OrderMenuItem
from restaurant.models import Table


class MenuView(FormView):

    template_name = 'menu.html'
    form_class = MenuForm

    def dispatch(self, request):
        self.success_url = reverse('menu')
        return super(MenuView, self).dispatch(request)

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

    def form_valid(self, form):
        d = form.cleaned_data

        # Place the order
        order = Order.objects.create(table=d['table'])
        for menuitem in d['menuitems']:
            OrderMenuItem.objects.create(
                order=order,
                menuitem=menuitem['menuitem'],
                quantity=menuitem['quantity']
            )

        return super(MenuView, self).form_valid(form)
