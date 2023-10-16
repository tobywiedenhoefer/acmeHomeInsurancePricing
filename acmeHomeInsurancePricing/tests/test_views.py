import json

from django.test import TestCase, Client
from django.urls import reverse

from acmeHomeInsurancePricing.models import Quote, QuoteRule, State
from acmeHomeInsurancePricing.shared.quote_algorithm import calculate_quote


class TestViews(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.state = State.objects.create(name="TestState", monthly_tax=0.5)
        self.coverage_type_rule = QuoteRule.objects.create(
            rule_name="coverage_type",
            value=20,
            on_value="Basic",
            is_multiplier=False,
            state=self.state,
        )
        self.flood_coverage_rule = QuoteRule.objects.create(
            rule_name="flood_coverage",
            value=0.01,
            on_value="True",
            is_multiplier=True,
            state=self.state,
        )
        self.valid_submission_fields_dict = {
            "owner_name": "TestOwner",
            "state": self.state.name,
            "coverage_type": "Basic",
            "flood_coverage": True,
            "has_pet": False,
        }
        self.valid_submission_fields = json.dumps(self.valid_submission_fields_dict)
        self.valid_quote = Quote.objects.create(
            owner_name="TestPerson",
            monthly_subtotal=2.22,
            monthly_taxes=1.11,
            rules=json.dumps({"coverage_type": "Test", "monthly_taxes": 0.5}),
        )
        self.submit_quote_url = reverse("submit_quote")

    def tearDown(self) -> None:
        self.state.delete()
        self.valid_quote.delete()

    def test_get_quote_VALID_ID(self):
        """
        Retreive a quote from a valid quote id.
        """
        url = reverse("get_quote", args=[self.valid_quote.pk])
        response = self.client.get(url)
        content = json.loads(response.content)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(self.valid_quote.pk, content.get("id"))
        self.assertEquals(2.22, content.get("monthly_subtotal"))
        self.assertEquals(1.11, content.get("monthly_taxes"))
        self.assertEquals(3.33, content.get("monthly_total"))
        self.assertEquals(dict, type(content.get("rules")))

        rules_applied = json.loads(self.valid_quote.rules)
        self.assertEqual(rules_applied, content.get("rules"))

    def test_get_quote_INVALID_ID(self):
        """
        Retreive a quote with an invalid quote id.
        """
        url = reverse("get_quote", args=[0])
        response = self.client.get(url)

        self.assertEquals(response.status_code, 404)
        self.assertEquals(json.loads(response.content), {})

    def test_submit_quote_VALID(self):
        """
        Submit a valid quote.
        """
        # calculate the quote from the view
        response = self.client.post(
            self.submit_quote_url,
            self.valid_submission_fields,
            content_type="application/json",
        )
        self.assertEquals(response.status_code, 201)
        content: dict = json.loads(response.content)

        # calculate the quote manually
        quote_dict = calculate_quote(
            json_req=json.loads(self.valid_submission_fields), state=self.state
        )

        self.assertListEqual(
            [
                "monthly_subtotal",
                "monthly_taxes",
                "monthly_total",
                "rules",
                "owner_name",
                "id",
            ],
            [key for key in content.keys()],
        )
        self.assertEquals(content["monthly_subtotal"], quote_dict["monthly_subtotal"])
        self.assertEquals(content["monthly_taxes"], quote_dict["monthly_taxes"])
        self.assertEquals(content["monthly_total"], quote_dict["monthly_total"])

    def test_submit_quote_INVALID_STATE(self):
        """
        Submit a quote for a state that does not exist.
        """
        invalid_state_submission_fields = self.valid_submission_fields_dict
        invalid_state_submission_fields["state"] = "InvalidState"
        response = self.client.post(
            self.submit_quote_url,
            invalid_state_submission_fields,
            content_type="application/json",
        )
        self.assertEquals(404, response.status_code)

    def test_submit_quote_INVALID_STATE_EMPTY(self):
        """
        Submit a quote for a state with an empty string.
        """
        invalid_state_submission_fields = self.valid_submission_fields_dict
        del invalid_state_submission_fields["state"]
        response = self.client.post(
            self.submit_quote_url,
            invalid_state_submission_fields,
            content_type="application/json",
        )
        self.assertEquals(422, response.status_code)

    def test_submit_quote_INVALID_REQUEST_BODY(self):
        """
        Submit a quote with an invalid request body: Either an empty string or invalid json structure.
        """
        response_empty_str_req_body = self.client.post(
            self.submit_quote_url, "", content_type="application/json"
        )
        response_invalid_json_req_body = self.client.post(
            self.submit_quote_url,
            self.valid_submission_fields.replace("{", ""),
            content_type="application/json",
        )
        self.assertEquals(400, response_empty_str_req_body.status_code)
        self.assertEquals(400, response_invalid_json_req_body.status_code)
