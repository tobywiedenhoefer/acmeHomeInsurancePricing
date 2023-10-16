import json
from typing import Optional

from django.db import models


class State(models.Model):
    """
    State model.
    :param name: 20-character max length of state/territory.
    :param monthly_tax: Monthly rate calculated after rule calculations.
    """

    name = models.CharField(max_length=20)
    monthly_tax = models.FloatField()

    def __str__(self) -> str:
        return self.name


class QuoteRule(models.Model):
    """
    Quote rules to add or multiply to the quote's running monthly subtotal on calculation.
    :param rule_name: The rule's name. Matches API request.
    :param value: Amount added/multiplied to the running monthly subtotal.
    :param on_value: Value is applied to monthly subtotal when on_value matches API request.
    :param is_multiplier: If true, value is multiplied to the subtotal at the end of calculation.
    :param state: State model.
    """

    rule_name = models.CharField(max_length=40)
    value = models.FloatField()
    on_value = models.CharField(max_length=40)
    is_multiplier = models.BooleanField()
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self) -> str:
        operator = "multiplies" if self.is_multiplier else "adds"
        value = 1 + self.value if self.is_multiplier else self.value
        return f"Rule<{self.state.name},{self.rule_name}> {operator} {value} when {self.on_value}"


class Quote(models.Model):
    """
    Outcome after quote calculation.
    :param owner_name: Name of person who owns/requested the quote for creation.
    :param monthly_subtotal: The product/sum after all quote rules have been applied.
    :param monthly_taxes: The monthly tax differed by state.
    :param rules: String Json representation of all rules applied to the quote.
    """

    owner_name = models.CharField(max_length=40)
    monthly_subtotal = models.FloatField()
    monthly_taxes = models.FloatField()
    rules = models.CharField(max_length=400)

    def __str__(self) -> str:
        return f"Quote<{self.pk}>(subtotal: {self.monthly_subtotal}, taxes: {self.monthly_taxes})"

    @property
    def monthly_total(self):
        return round(self.monthly_subtotal + self.monthly_taxes, 3)

    @property
    def rules_to_json_dict(self) -> Optional[dict]:
        try:
            return json.loads(self.rules)
        except Exception as _:
            return None
