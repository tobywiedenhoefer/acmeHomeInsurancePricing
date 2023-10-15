import json
from typing import List

from django.http import JsonResponse
from django.http import HttpRequest

from rest_framework.decorators import api_view

from .models import Quote, State, QuoteRule
from .serializers import QuoteSerializer
from .shared.quote_algorithm import calculate_quote


INVALID_METHOD = JsonResponse({"message": "Invalid Method"}, status=405)


@api_view(("GET",))
def get_quote(request: HttpRequest, quote_id):
    """
    Get a stored quote from a quote_id
    :param request: HttpRequest.
    :param quote_id: Quote id.
    :return: JsonResponse
    """
    if request.method != "GET":
        return INVALID_METHOD
    try:
        quote = Quote.objects.get(pk=quote_id)
        serialized = QuoteSerializer(quote)
        return JsonResponse(serialized.data, safe=False)
    except Quote.DoesNotExist:
        return JsonResponse({}, status=404)


@api_view(("POST",))
def submit_quote(request: HttpRequest):
    """
    Using the information provided, create a quote, store it in the DB, and return to user.
    :param request: HttpRequest
    :return: JsonResponse
    """
    try:
        body = request.body.decode("utf-8")
        json_req = json.loads(body)
    except json.decoder.JSONDecodeError:
        return JsonResponse({"message": "Request body must be JSON."}, status=400)
    except Exception as e:
        print("Unknown error:", e)
        return JsonResponse({"message": "An unknown error has occurred."}, status=500)

    state_name = json_req.get("state", None)
    if not state_name:
        return JsonResponse({"message": "Request must include state."}, status=422)

    try:
        state: State = State.objects.filter(name=state_name).first()
        if not state:
            raise State.DoesNotExist
    except State.DoesNotExist:
        return JsonResponse({"message": "Requested is not supported."}, status=404)

    quote_dict = calculate_quote(json_req=json_req, state=state)

    try:
        json_str = json.dumps(rules_applied)
        quote = Quote.objects.create(
            monthly_subtotal=quote_subtotal, monthly_taxes=taxes, rules=json_str
        )
    except Exception as e:
        return JsonResponse(
            {"message": "An error arrised while creating quote id."}, status=500
        )

    result = {
        "quote_id": quote.pk,
        "monthly_subtotal": quote_subtotal,
        "monthly_tax": taxes,
        "monthly_total": quote_subtotal + taxes,
    }

    return JsonResponse(result)
