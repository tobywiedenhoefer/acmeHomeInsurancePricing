import json

from django.test import TestCase

from acmeHomeInsurancePricing.models import State, Quote, QuoteRule


class TestModels(TestCase):
    def setUp(self) -> None:
        self.state = State.objects.create(name="TestState", monthly_tax=0.5)
        self.quote_rules_dict = {
            "coverage_type": "Test",
            "has_pet": True,
        }
        self.quote = Quote.objects.create(
            owner_name="TestOwner",
            monthly_subtotal=2.22,
            monthly_taxes=1.11,
            rules=json.dumps(self.quote_rules_dict),
        )
        self.coverage_type_rule = QuoteRule.objects.create(
            rule_name="coverage_type",
            value=2.22,
            on_value="Test",
            is_multiplier=False,
            state=self.state,
        )

    def tearDown(self) -> None:
        self.state.delete()
        self.quote.delete()

    def test_get_state_by_name(self):
        """
        Get state by name using filter and then the 'first' shortcut.
        """
        state = State.objects.filter(name=self.state.name).first()
        self.assertIsNotNone(state)
        self.assertEquals(self.state.pk, state.pk)
        self.assertEquals(self.state.monthly_tax, state.monthly_tax)

    def test_get_quote_by_id(self):
        """
        Get quote by quote id.
        """
        quote = Quote.objects.get(pk=self.quote.pk)
        self.assertEqual(self.quote.pk, quote.pk)
        self.assertEqual(self.quote.owner_name, quote.owner_name)
        self.assertEquals(self.quote.monthly_subtotal, quote.monthly_subtotal)
        self.assertEquals(self.quote.monthly_taxes, quote.monthly_taxes)
        self.assertEquals(self.quote.rules, quote.rules)
        self.assertEquals(self.quote.monthly_total, quote.monthly_total)

    def test_get_coverage_type_rule_by_state(self):
        """
        Get coverage type rule by state.
        """
        rules = QuoteRule.objects.filter(state=self.state)
        self.assertEquals(len(rules), 1)
        coverage_type_rule = rules.first()
        self.assertEquals(
            self.coverage_type_rule.rule_name, coverage_type_rule.rule_name
        )
        self.assertEquals(self.coverage_type_rule.value, coverage_type_rule.value)
        self.assertEquals(self.coverage_type_rule.on_value, coverage_type_rule.on_value)
        self.assertEquals(
            self.coverage_type_rule.is_multiplier, coverage_type_rule.is_multiplier
        )
        self.assertEquals(self.coverage_type_rule.state, coverage_type_rule.state)
        self.assertEquals(self.state, coverage_type_rule.state)
