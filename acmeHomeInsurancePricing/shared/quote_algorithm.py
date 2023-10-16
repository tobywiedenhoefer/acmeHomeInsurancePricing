import json
from typing import List

from acmeHomeInsurancePricing.models import QuoteRule, State


def calculate_quote(json_req: dict, state: State) -> dict:
    """
    Return a dictionary with the quote's subtotal, monthly taxes, and the rules that were applied to the quote.
    :param json_req: A dictionary with the request's body.
    :param state: A state model for the requested quote.
    :return: A dictionary with monthly_subtotal, monthly_taxes, monthly_total, and rules keys.
    """
    quote_subtotal = 0
    multiplier = 1
    rules_applied = json_req
    if "owner_name" in json_req:
        del rules_applied["owner_name"]

    rules: List[QuoteRule] = QuoteRule.objects.filter(state=state)
    for rule in rules:
        if rule.rule_name not in json_req:
            continue

        req_value = json_req[rule.rule_name]
        if str(req_value) != rule.on_value:
            continue

        if rule.is_multiplier:
            multiplier *= 1 + rule.value
        else:
            quote_subtotal += rule.value

    quote_subtotal *= multiplier
    monthly_taxes = quote_subtotal * state.monthly_tax
    rules_applied["state"] = state.name
    rules_applied["monthly_taxes"] = state.monthly_tax
    rules_applied_str = json.dumps(rules_applied)
    return {
        "monthly_subtotal": quote_subtotal,
        "monthly_taxes": monthly_taxes,
        "monthly_total": round(quote_subtotal + monthly_taxes, 3),
        "rules": rules_applied_str,
    }
