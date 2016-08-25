"""
:Created: 24 August 2016
:Author: Lucas Connors

"""

from seared_quail.tests import SearedQuailTestCase


class OrderWebTestCase(SearedQuailTestCase):

    def get200s(self):
        return [
            '/kitchen/',
        ]
