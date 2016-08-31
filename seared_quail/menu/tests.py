"""
:Created: 24 August 2016
:Author: Lucas Connors

"""

from menu.models import Category, MenuItem
from restaurant.models import Table
from seared_quail.tests import SearedQuailTestCase, MigrationTestCase


class MenuItemInitialOrdersMigrationTestCase(MigrationTestCase):

    migrate_from = '0003_auto_20150514_2203'
    migrate_to = '0005_auto_20160829_0618'

    def setUpBeforeMigration(self, apps):
        # Create a category for the menu item
        Category = apps.get_model('menu', 'Category')
        category = Category.objects.create(name='Appetizers')

        # Create a menu item
        MenuItem = apps.get_model('menu', 'MenuItem')
        self.premigration_menuitem = MenuItem.objects.create(category=category, name='House Salad')

    def testInstancesHaveInitialOrder(self):
        MenuItem = self.apps.get_model('menu', 'MenuItem')
        menuitem = MenuItem.objects.get(id=self.premigration_menuitem.id)
        self.assertEquals(menuitem.order, menuitem.id)


class CategoryInitialOrdersMigrationTestCase(MigrationTestCase):

    migrate_from = '0006_category_parent'
    migrate_to = '0008_auto_20160829_0622'

    def setUpBeforeMigration(self, apps):
        Category = apps.get_model('menu', 'Category')
        self.premigration_category = Category.objects.create(name='Appetizers')

    def testCategoriesHaveInitialOrder(self):
        Category = self.apps.get_model('menu', 'Category')
        category = Category.objects.get(id=self.premigration_category.id)
        self.assertEquals(category.order, category.id)


class MenuAdminWebTestCase(SearedQuailTestCase):

    def get200s(self):
        return [
            '/admin/menu/',
            '/admin/menu/category/',
            '/admin/menu/category/add/',
            '/admin/menu/category/{category_id}/change/'.format(category_id=self.category.id),
            '/admin/menu/menuitem/',
            '/admin/menu/menuitem/add/',
            '/admin/menu/menuitem/{menu_item_id}/change/'.format(menu_item_id=self.menu_item.id),
        ]

    def testCategoryCannotBeAncestorOfSelf(self):
        # Create a new category, which is a subcategory of Drinks
        data = {
            'name': 'Juices',
            'parent': self.category.id,
        }
        self.assertResponseRedirects('/admin/menu/category/add/', '/admin/menu/category/', method='POST', data=data)
        juices_category = Category.objects.get(name='Juices')

        # Attempt to change the Drinks category to be a
        # subcategory of Juices, that shouldn't work
        url = '/admin/menu/category/{category_id}/change/'.format(category_id=self.category.id)
        data = {
            'name': self.category.name,
            'parent': juices_category.id,
        }
        self.assertResponseRenders(url, method='POST', data=data, has_form_error=True)

        # But Drinks can be a category without a parent
        del data['parent']
        self.assertResponseRedirects(url, '/admin/menu/category/', method='POST', data=data)

    def testUserCanOrderMenuItemSetting(self):
        # A user cannot order an item that's not on the menu
        url = '/admin/menu/menuitem/{menu_item_id}/change/'.format(menu_item_id=self.menu_item.id)
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
