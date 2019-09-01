"""
:Created: 24 August 2016
:Author: Lucas Connors

"""

from seared_quail.tests import SearedQuailTestCase


class RestaurantAdminWebTestCase(SearedQuailTestCase):
    def get200s(self):
        return [
            "/admin/restaurant/",
            "/admin/restaurant/table/",
            "/admin/restaurant/table/add/",
            "/admin/restaurant/table/{table_id}/change/".format(table_id=self.table.id),
        ]
