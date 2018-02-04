"""
:Created: 24 August 2016
:Author: Lucas Connors

"""

from django.apps import apps
from django.contrib.auth.models import User
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TestCase

from pigeon.test import RenderTestCase

from menu.models import Category, MenuItem
from order.models import Order, OrderMenuItem
from restaurant.models import Table


class SearedQuailTestCase(RenderTestCase):

    USER_USERNAME = 'jsmith'
    USER_EMAIL = 'jsmith@example.com'
    USER_PASSWORD = 'abc123'

    CATEGORY_NAME = 'Drinks'
    SUBCATEGORY_NAME = 'Soda'
    MENU_ITEM_NAME = 'Water'
    MENU_ITEM_IN_SUBCATEGORY_NAME = 'Cola'
    TABLE_NUMBER = 'A-1'

    def setUp(self):
        super(SearedQuailTestCase, self).setUp()

        # Create admin user
        self.user = User.objects.create_user(self.USER_USERNAME, email=self.USER_EMAIL, password=self.USER_PASSWORD)
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()
        self.client.login(username=self.USER_USERNAME, password=self.USER_PASSWORD)

        # Create initial instances
        self.category = Category.objects.create(name=self.CATEGORY_NAME)
        self.menu_item = MenuItem.objects.create(category=self.category, name=self.MENU_ITEM_NAME)
        self.subcategory = Category.objects.create(name=self.SUBCATEGORY_NAME, parent=self.category)
        self.menu_item_in_subcategory = MenuItem.objects.create(
            category=self.subcategory,
            name=self.MENU_ITEM_IN_SUBCATEGORY_NAME
        )
        self.table = Table.objects.create(number=self.TABLE_NUMBER)

        # Place an order
        self.order = Order.objects.create(table=self.table)
        OrderMenuItem.objects.create(order=self.order, menuitem=self.menu_item)


class MigrationTestCase(TestCase):
    """
    Ref: https://www.caktusgroup.com/blog/2016/02/02/writing-unit-tests-django-migrations/
    """

    migrate_from = None
    migrate_to = None

    @property
    def app(self):
        return apps.get_containing_app_config(type(self).__module__).name

    def setUp(self):
        # Verify that migration_from and migration_to are defined
        assertion_error_message = (
            "MigrationTestCase '{test_case_name}' must define migrate_from and migrate_to properties."
        ).format(test_case_name=type(self).__name__)
        assert self.migrate_from and self.migrate_to, assertion_error_message

        # Init MigrationExecutor
        self.migrate_from = [(self.app, self.migrate_from)]
        self.migrate_to = [(self.app, self.migrate_to)]
        executor = MigrationExecutor(connection)
        old_apps = executor.loader.project_state(self.migrate_from).apps

        # Reverse to old migration
        executor.migrate(self.migrate_from)

        # Create model instances before migration runs
        self.setUpBeforeMigration(old_apps)

        # Run the migration to test
        executor = MigrationExecutor(connection)
        executor.loader.build_graph()
        executor.migrate(self.migrate_to)
        self.apps = executor.loader.project_state(self.migrate_to).apps

    def setUpBeforeMigration(self, apps):
        pass


class AdminWebTestCase(SearedQuailTestCase):

    def get200s(self):
        return [
            '/admin/',
        ]

    def testAdminLoginPageRenders(self):
        self.client.logout()
        self.assertResponseRedirects('/admin/', '/admin/login/')
