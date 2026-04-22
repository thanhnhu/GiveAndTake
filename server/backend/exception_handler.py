from rest_framework.views import exception_handler
from rest_framework import status
from requests import ConnectionError, HTTPError
# from rest_framework.response import Response
from django.http import JsonResponse
import logging


def global_exception_handler(exc, context):
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    # logs detail data from the exception being handled
    logging.error(f"Original error detail and callstack: {exc}")

    if response is None:
        # defines custom response data
        err_data = {
            'isSuccess': False,
            'error': 'Internal Server Error'
        }
        # returns a JsonResponse
        return JsonResponse(err_data, safe=False, status=500)

    # checks if the raised exception is of the type you want to handle
    if isinstance(exc, ConnectionError):
        # defines custom response data
        err_data = {
            'isSuccess': False,
            'error': 'Internal Server Error'
        }
        # returns a JsonResponse
        return JsonResponse(err_data, safe=False, status=503)

    if isinstance(exc, HTTPError):
        # defines custom response data
        err_data = {
            'isSuccess': False,
            'error': 'Internal Server Error'
        }
        # returns a JsonResponse
        return JsonResponse(err_data, safe=False, status=500)

    # returns response as handled normally by the framework
    return response
