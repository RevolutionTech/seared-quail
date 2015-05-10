"""
:Created: 10 May 2015
:Author: Lucas Connors

"""

import datetime

from django.http import HttpResponse
from django.views.generic import TemplateView

from order.forms import OrderCompleteForm
from order.models import Order


class KitchenView(TemplateView):

    template_name = 'kitchen.html'

    def get_context_data(self, **kwargs):
        context = super(KitchenView, self).get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(completed__isnull=True).order_by('id')
        return context


def complete_order(request):
    form = OrderCompleteForm(request.POST)
    if form.is_valid():
        order = form.cleaned_data['order']
        order.completed = datetime.datetime.now()
        order.save()
        return HttpResponse("")

    return HttpResponse(status=500)
