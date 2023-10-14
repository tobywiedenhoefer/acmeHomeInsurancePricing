from django.test import SimpleTestCase
from django.urls import reverse, resolve

from acmeHomeInsurancePricing.views import get_quote, submit_quote


class TestUrls(SimpleTestCase):
    def test_get_quote_url_is_resolved(self):
        url = reverse("get_quote", args=[1])
        self.assertEquals(resolve(url).func, get_quote)

    def test_submit_quote_url_is_resolved(self):
        url = reverse("submit_quote")
        self.assertEquals(resolve(url).func, submit_quote)
