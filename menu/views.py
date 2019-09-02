"""
:Created: 5 May 2015
:Author: Lucas Connors

"""

from django.contrib import messages
from django.urls import reverse
from django.views.generic.edit import FormView

from menu.forms import MenuForm
from menu.models import Category
from order.models import Order, OrderMenuItem
from order.sockets import _connections
from restaurant.models import Table


class MenuView(FormView):

    template_name = "menu.html"
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
            encoded_category["subcategories"] = subcategories

        # Encode this category
        if category.menuitem_set.filter(show_in_menu=True).exists():
            encoded_category.update(
                {
                    "name": category.name,
                    "description": category.description,
                    "menuitems": category.menuitem_set.filter(
                        show_in_menu=True
                    ).order_by("order"),
                }
            )
        return encoded_category

    def get_success_url(self):
        return reverse("menu")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Collect menu items
        menu = []
        for category in Category.objects.filter(parent__isnull=True).order_by("order"):
            encoded_category = self.encode_category(category)
            if encoded_category:
                menu.append(encoded_category)

        context["menu"] = menu
        context["tables"] = Table.objects.all()

        return context

    def form_valid(self, form):
        d = form.cleaned_data

        # Place the order
        order = Order.objects.create(table=d["table"])
        for menuitem in d["menuitems"]:
            OrderMenuItem.objects.create(
                order=order,
                menuitem=menuitem["menuitem"],
                quantity=menuitem["quantity"],
                note=menuitem["note"],
            )

        # Notify kitchen(s)
        for connection_id, connection in _connections.items():
            connection.emit("update")

        # Write success message to session
        messages.success(self.request, "Your order has been placed.")

        return super().form_valid(form)
