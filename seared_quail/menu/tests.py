"""
:Created: 24 August 2016
:Author: Lucas Connors

"""

from menu.models import Category, MenuItem
from restaurant.models import Table
from seared_quail.tests import SearedQuailTestCase, MigrationTestCase


class MenuSetInitialOrdersMigrationTestCase(MigrationTestCase):

    migrate_from = '0003_auto_20150514_2203'
    migrate_to = '0006_auto_20150527_0215'

    def setUpBeforeMigration(self, apps):
        Category = apps.get_model('menu', 'Category')
        MenuItem = apps.get_model('menu', 'MenuItem')
        self.premigration_category = Category.objects.create(name='Appetizers')
        self.premigration_menuitem = MenuItem.objects.create(category=self.premigration_category, name='House Salad')

    def testInstancesHaveInitialOrder(self):
        Category = self.apps.get_model('menu', 'Category')
        MenuItem = self.apps.get_model('menu', 'MenuItem')
        category = Category.objects.get(id=self.premigration_category.id)
        menuitem = MenuItem.objects.get(id=self.premigration_menuitem.id)
        self.assertEquals(category.order, category.id)
        self.assertEquals(menuitem.order, menuitem.id)


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

    def construct_initial_order_data(self):
        data = {'table': self.table.id}
        for menu_item in MenuItem.objects.all():
            data['quantity-{menu_item_id}'.format(menu_item_id=menu_item.id)] = 0
        return data

    def get200s(self):
        return [
            '/',
        ]

    def testMenuUnauthenticated(self):
        self.client.logout()
        self.assertResponseRenders('/')

    def testPlaceOrder(self):
        data = self.construct_initial_order_data()
        data['quantity-{menu_item_id}'.format(menu_item_id=self.menu_item.id)] = 1
        self.assertResponseRenders('/')
        self.assertResponseRedirects('/', '/', method='POST', data=data)

    def testOrderFromInvalidTableFails(self):
        invalid_table_id = Table.objects.all().order_by('-id')[0].id + 1
        data = self.construct_initial_order_data()
        data['table'] = invalid_table_id
        self.assertResponseRenders('/', method='POST', data=data, has_form_error=True)

    def testOrderForUnavailableMenuItem(self):
        # The user loads the menu and prepares an order
        self.assertResponseRenders('/')
        data = self.construct_initial_order_data()
        data['quantity-{menu_item_id}'.format(menu_item_id=self.menu_item.id)] = 1

        # Unfortunately, the item just became unavailable
        self.menu_item.user_can_order = False
        self.menu_item.save()

        # The user submits their order, but it is unsuccessful
        # and they need to revise their order
        self.assertResponseRenders('/', method='POST', data=data, has_form_error=True)
