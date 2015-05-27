"""
:Created: 5 May 2015
:Author: Lucas Connors

"""

from django.core.urlresolvers import reverse
from django.views.generic.edit import FormView


from menu.models import Category
from menu.forms import MenuForm
from order.models import Order, OrderMenuItem
from order.sockets import _connections
from restaurant.models import Table


class MenuView(FormView):

    template_name = 'menu.html'
    form_class = MenuForm

    @classmethod
    def encode_category(cls, category):
        encoded_category = {}

        # Recursively get subcategories
        subcategories = []
        for subcategory in Category.objects.filter(parent=category):
            encoded_subcategory = cls.encode_category(subcategory)
            if encoded_subcategory:
                subcategories.append(encoded_subcategory)
        if subcategories:
            encoded_category['subcategories'] = subcategories

        # Encode this category
        if category.menuitem_set.filter(enabled=True).exists():
            encoded_category.update({
                'name': category.name,
                'description': category.description,
                'menuitems': category.menuitem_set.filter(enabled=True).order_by('order'),
            })
        return encoded_category

    def dispatch(self, request):
        self.success_url = reverse('menu') + '?success=1'
        return super(MenuView, self).dispatch(request)

    def get_context_data(self, **kwargs):
        context = super(MenuView, self).get_context_data(**kwargs)

        # Collect menu items
        menu = []
        for category in Category.objects.filter(parent__isnull=True).order_by('order'):
            encoded_category = self.encode_category(category)
            if encoded_category:
                menu.append(encoded_category)

        context['menu'] = menu
        context['tables'] = Table.objects.all()
        if self.request.GET.get('success', False):
            context['success'] = True

        return context

    def form_valid(self, form):
        d = form.cleaned_data

        # Place the order
        order = Order.objects.create(table=d['table'])
        for menuitem in d['menuitems']:
            OrderMenuItem.objects.create(
                order=order,
                menuitem=menuitem['menuitem'],
                quantity=menuitem['quantity'],
                note=menuitem['note']
            )

        # Notify kitchen(s)
        for connection_id, connection in _connections.iteritems():
            connection.emit('update')

        return super(MenuView, self).form_valid(form)
