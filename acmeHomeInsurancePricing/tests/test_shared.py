import json

from django.test import TestCase, Client
from django.urls import reverse, resolve

from acmeHomeInsurancePricing.models import State, QuoteRule
from acmeHomeInsurancePricing.shared.quote_algorithm import calculate_quote


class TestShared(TestCase):
    def setUp(self) -> None:
        self.client = Client
        self.state = State.objects.create(name="Testing State", monthly_tax=0.5)
        self.coverage_rule = QuoteRule.objects.create(
            rule_name="coverage_type",
            value=5,
            on_value="Basic",
            is_multiplier=False,
            state=self.state,
        )
        self.pet_rule = QuoteRule.objects.create(
            rule_name="has_pet",
            value=3,
            on_value="True",
            is_multiplier=False,
            state=self.state,
        )
        self.flood_coverage = QuoteRule.objects.create(
            rule_name="flood_coverage",
            value=0.3,
            on_value="True",
            is_multiplier=True,
            state=self.state,
        )

    def tearDown(self) -> None:
        self.state.delete()  # deletes all QuoteRules with cascading

    def test_calculate_quote(self):
        """
        Test the shared calculate_quote function.
        """
        req_dict = {
            "owner_name": "TestOwner",
            "coverage_type": "Basic",
            "has_pet": True,
            "flood_coverage": True,
        }
        quote_dict = calculate_quote(json_req=req_dict, state=self.state)
        rules_resp = json.loads(quote_dict["rules"])

        # calculate manually
        subtotal = self.coverage_rule.value + self.pet_rule.value
        subtotal *= 1 + self.flood_coverage.value
        req_dict["state"] = self.state.name
        taxes = subtotal * self.state.monthly_tax

        self.assertListEqual(
            ["monthly_subtotal", "monthly_taxes", "monthly_total", "rules"],
            [key for key in quote_dict.keys()],
        )
        self.assertEquals(subtotal, quote_dict["monthly_subtotal"])
        self.assertEquals(taxes, quote_dict["monthly_taxes"])

        # adding as monthly taxes could be subject to change
        req_dict["monthly_taxes"] = self.state.monthly_tax
        self.assertDictEqual(req_dict, rules_resp)
