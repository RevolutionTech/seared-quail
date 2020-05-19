"""
:Created: 10 May 2015
:Author: Lucas Connors

"""

import functools
import json

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
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
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("kitchen"))
        return func(request, *args, **kwargs)

    return wrapper


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse("login"))


class LoginView(FormView):

    template_name = "login.html"
    form_class = LoginForm

    def get_success_url(self):
        return self.request.GET.get("next", reverse("kitchen"))

    def form_valid(self, form):
        d = form.cleaned_data
        username, password = d["username"], d["password"]
        user = authenticate(username=username, password=password)
        if user:
            auth_login(self.request, user)
            return super().form_valid(form)


class KitchenView(TemplateView):

    template_name = "kitchen.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = Order.objects.all()
        context["orders"] = {
            "submitted": [
                order.encodeJSON()
                for order in orders.filter(completed__isnull=True).order_by("id")
            ],
            "completed": [
                order.encodeJSON()
                for order in orders.filter(completed__isnull=False).order_by("-id")
            ],
        }
        return context


@login_required
def update_orders(request):
    last_order_id = request.GET.get("lastorder", 0)
    new_orders = Order.objects.filter(id__gt=last_order_id, completed__isnull=True)
    return JSONResponse([order.encodeJSON() for order in new_orders])


@login_required
def complete_order(request):
    form = OrderCompleteForm(request.POST)
    if form.is_valid():
        order = form.cleaned_data["order"]
        order.completed = timezone.now()
        order.save()
        return HttpResponse("")

    return HttpResponseNotFound("Provided order ID does not exist.")
