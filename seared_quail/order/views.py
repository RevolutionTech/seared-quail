"""
:Created: 10 May 2015
:Author: Lucas Connors

"""

from django.views.generic import TemplateView

from order.models import Order


class KitchenView(TemplateView):

    template_name = 'kitchen.html'

    def get_context_data(self, **kwargs):
        context = super(KitchenView, self).get_context_data(**kwargs)
        context['orders'] = Order.objects.all().order_by('id')
        return context
