"""
:Created: 24 August 2016
:Author: Lucas Connors

"""

from django.test import TestCase


class SearedQuailTestCase(TestCase):

    def assertResponseRenders(self, url, status_code=200, method='GET', data={}, has_form_error=False, **kwargs):
        request_method = getattr(self.client, method.lower())
        follow = status_code == 302
        response = request_method(url, data=data, follow=follow, **kwargs)

        if status_code == 302:
            redirect_url, response_status_code = response.redirect_chain[0]
        else:
            response_status_code = response.status_code
        self.assertEquals(
            response_status_code,
            status_code,
            "URL {url} returned with status code {actual_status} when {expected_status} was expected.".format(
                url=url,
                actual_status=response_status_code,
                expected_status=status_code
            )
        )

        # Check that forms submitted did not return errors (or did if it should have)
        form_error_assertion_method = self.assertIn if has_form_error else self.assertNotIn
        form_error_assertion_method('errorlist', response.content)

        return response

    def get200s(self):
        return []

    def testRender200s(self):
        for url in self.get200s():
            self.assertResponseRenders(url)
