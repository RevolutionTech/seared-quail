"""
:Created: 24 August 2016
:Author: Lucas Connors

"""

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
