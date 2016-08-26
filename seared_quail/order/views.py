"""
:Created: 10 May 2015
:Author: Lucas Connors

"""

import functools
import json

from django.contrib.auth import authenticate, login as auth_login, \
    logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from order.forms import LoginForm, OrderCompleteForm
from order.models import Order


def JSONResponse(obj):
    return HttpResponse(json.dumps(obj, indent=2), content_type="application/json")


def redirect_authenticated(func):
    """ If the user is already authenticated, redirect to kitchen """

    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('kitchen'))
        return func(request, *args, **kwargs)

    return wrapper


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('login'))


class LoginView(FormView):

    template_name = 'login.html'
    form_class = LoginForm

    def dispatch(self, request):
        self.success_url = request.GET.get('next', reverse('kitchen'))
        return super(LoginView, self).dispatch(request)

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['redirect_url'] = self.success_url
        return context

    def form_valid(self, form):
        d = form.cleaned_data
        username, password = d['username'], d['password']
        user = authenticate(username=username, password=password)
        if user:
            auth_login(self.request, user)
            return super(LoginView, self).form_valid(form)


class KitchenView(TemplateView):

    template_name = 'kitchen.html'

    def get_context_data(self, **kwargs):
        context = super(KitchenView, self).get_context_data(**kwargs)
        orders = Order.objects.all()
        context['orders'] = {
            'submitted': [order.encodeJSON() for order in orders.filter(completed__isnull=True).order_by('id')],
            'completed': [order.encodeJSON() for order in orders.filter(completed__isnull=False).order_by('-id')],
        }
        return context


@login_required
def update_orders(request):
    last_order_id = request.GET.get('lastorder', 0)
    new_orders = Order.objects.filter(id__gt=last_order_id, completed__isnull=True)
    return JSONResponse([order.encodeJSON() for order in new_orders])


@login_required
def complete_order(request):
    form = OrderCompleteForm(request.POST)
    if form.is_valid():
        order = form.cleaned_data['order']
        order.completed = timezone.now()
        order.save()
        return HttpResponse("")

    return HttpResponse(status=500)
