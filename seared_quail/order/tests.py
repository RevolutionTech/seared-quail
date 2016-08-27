"""
:Created: 24 August 2016
:Author: Lucas Connors

"""

from order.models import Order
from seared_quail.tests import SearedQuailTestCase


class AuthWebTestCase(SearedQuailTestCase):

    def testLogout(self):
        self.assertResponseRedirects('/logout/', '/login')

    def testLogin(self):
        self.client.logout()
        login_data = {
            'username': self.USER_USERNAME,
            'password': self.USER_PASSWORD,
        }
        self.assertResponseRedirects('/login/', '/kitchen', method='POST', data=login_data)

    def testLoginWithEmail(self):
        self.client.logout()
        login_data = {
            'username': self.USER_EMAIL,
            'password': self.USER_PASSWORD,
        }
        self.assertResponseRedirects('/login/', '/kitchen', method='POST', data=login_data)

    def testUserDoesNotExist(self):
        self.client.logout()

        # Fail to log in with invalid username
        login_data = {
            'username': 'does-not-exist',
            'password': self.USER_PASSWORD,
        }
        self.assertResponseRenders('/login/', method='POST', data=login_data, has_form_error=True)

        # Fail to log in with invalid email
        login_data['username'] = 'does_not_exist@example.com'
        self.assertResponseRenders('/login/', method='POST', data=login_data, has_form_error=True)


class OrderWebTestCase(SearedQuailTestCase):

    def get200s(self):
        return [
            '/kitchen/',
            '/kitchen/update/',
        ]

    def testMarkOrderComplete(self):
        num_pending_orders = Order.objects.filter(completed__isnull=True).count()
        self.assertResponseRenders('/kitchen/completeorder/', method='POST', data={'order': self.order.id})
        self.assertEquals(Order.objects.filter(completed__isnull=True).count(), num_pending_orders - 1)
