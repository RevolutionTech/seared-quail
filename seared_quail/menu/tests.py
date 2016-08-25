"""
:Created: 24 August 2016
:Author: Lucas Connors

"""

from menu.models import MenuItem
from seared_quail.tests import SearedQuailTestCase


class MenuAdminWebTestCase(SearedQuailTestCase):

    def get200s(self):
        return [
            '/admin/menu/',
            '/admin/menu/category/',
            '/admin/menu/category/add/',
            '/admin/menu/category/{category_id}/'.format(category_id=self.category.id),
            '/admin/menu/menuitem/',
            '/admin/menu/menuitem/add/',
            '/admin/menu/menuitem/{menu_item_id}/'.format(menu_item_id=self.menu_item.id),
        ]


class MenuWebTestCase(SearedQuailTestCase):

    def get200s(self):
        return [
            '/',
        ]

    def testMenuUnauthenticated(self):
        self.client.logout()
        self.assertResponseRenders('/')

    def testPlaceOrder(self):
        # Construct POST data for placing an order
        place_order_data = {'table': self.table.id}
        for menu_item in MenuItem.objects.all():
            place_order_data['quantity-{menu_item_id}'.format(menu_item_id=menu_item.id)] = 0
        place_order_data['quantity-{menu_item_id}'.format(menu_item_id=self.menu_item.id)] = 1

        self.assertResponseRenders('/')
        self.assertResponseRedirects('/', '/', method='POST', data=place_order_data)
