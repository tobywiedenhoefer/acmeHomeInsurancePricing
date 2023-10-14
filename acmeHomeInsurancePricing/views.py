from django.http import JsonResponse
from django.http import HttpRequest
import json

from rest_framework.decorators import api_view

from .models import Quotes
from .serializers import QuoteSerializer


INVALID_METHOD = JsonResponse({"message": "Invalid Method"}, status=405)


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
        quote = Quotes.objects.get(pk=quote_id)
        serialized = QuoteSerializer(quote)
        return JsonResponse(serialized.data, safe=False)
    except Quotes.DoesNotExist:
        return JsonResponse({}, status=404)


@api_view(('POST',))
def post_quote(request: HttpRequest):
    """
    Using the information provided, create a quote, store it in the DB, and return to user.
    :param request: HttpRequest
    :return: JsonResponse
    """
    if request.method != "POST":
        return INVALID_METHOD

    try:
        body = request.body.decode('utf-8')
        json_req = json.loads(body)
    except json.decoder.JSONDecodeError:
        return JsonResponse({"message": "Request body must be JSON."}, status=400)
    except Exception as e:
        print("Unknown error:", e)
        return JsonResponse({"message": "An unknown error has occurred."}, status=500)

    state = json_req["state"]


    return JsonResponse({})


