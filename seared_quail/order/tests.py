"""
:Created: 24 August 2016
:Author: Lucas Connors

"""

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


class OrderWebTestCase(SearedQuailTestCase):

    def get200s(self):
        return [
            '/kitchen/',
        ]
