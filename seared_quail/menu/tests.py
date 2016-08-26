"""
:Created: 24 August 2016
:Author: Lucas Connors

"""

from menu.models import Category, MenuItem
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

    def testCategoryCannotBeAncestorOfSelf(self):
        # Create a new category, which is a subcategory of Entrees
        data = {
            'name': 'Sandwiches',
            'parent': self.category.id,
        }
        self.assertResponseRedirects('/admin/menu/category/add/', '/admin/menu/category/', method='POST', data=data)
        sandwiches_category = Category.objects.get(name='Sandwiches')

        # Attempt to change the Entrees category to be a
        # subcategory of Sandwiches, that shouldn't work
        url = '/admin/menu/category/{category_id}/'.format(category_id=self.category.id)
        data = {
            'name': self.category.name,
            'parent': sandwiches_category.id,
        }
        self.assertResponseRenders(url, method='POST', data=data, has_form_error=True)

        # But Entrees can be a category without a parent
        del data['parent']
        self.assertResponseRedirects(url, '/admin/menu/category/', method='POST', data=data)

    def testUserCanOrderMenuItemSetting(self):
        # A user cannot order an item that's not on the menu
        url = '/admin/menu/menuitem/{menu_item_id}/'.format(menu_item_id=self.menu_item.id)
        data = {
            'category': self.category.id,
            'name': 'Soup of the Day',
            'show_in_menu': False,
            'user_can_order': True,
        }
        self.assertResponseRenders(url, method='POST', data=data, has_form_error=True)

        # But if we disable the user from being able to order the item,
        # then there's no problem if it's not on the menu
        data['user_can_order'] = False
        self.assertResponseRedirects(url, '/admin/menu/menuitem/', method='POST', data=data)


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
