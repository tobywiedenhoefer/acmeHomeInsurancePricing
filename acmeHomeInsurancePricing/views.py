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
        data = serialized.data
        data["rules"] = json.loads(data["rules"])
        data["monthly_total"] = quote.monthly_total
        data["quote_id"] = data["id"]
        del data["id"]
        return JsonResponse(data)
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
    except Exception as _:
        return JsonResponse({"message": "An unknown error has occurred."}, status=500)

    state_name = json_req.get("state", None)
    owner_name = json_req.get("owner_name", None)
    if not state_name:
        return JsonResponse(
            {"message": "Request must include a state name."}, status=422
        )
    elif not owner_name:
        return JsonResponse(
            {"message": "Request must include an owner/buyer name."}, status=422
        )

    try:
        state: State = State.objects.filter(name=state_name).first()
        if not state:
            raise State.DoesNotExist
    except State.DoesNotExist:
        return JsonResponse({"message": "Requested is not supported."}, status=404)

    quote_dict = calculate_quote(json_req=json_req, state=state)

    try:
        quote = Quote.objects.create(
            owner_name=owner_name,
            monthly_subtotal=quote_dict["monthly_subtotal"],
            monthly_taxes=quote_dict["monthly_taxes"],
            rules=quote_dict["rules"],
        )
    except Exception as e:
        return JsonResponse(
            {"message": "An error arrised while creating quote id."}, status=500
        )

    quote_dict["owner_name"] = owner_name
    quote_dict["quote_id"] = quote.pk
    quote_dict["rules"] = json.loads(quote_dict["rules"])

    return JsonResponse(quote_dict, status=201)
