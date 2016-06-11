"""Descriptive message and response code for all error"""
from mongoengine import *
from . import json_response
import json


class MethodError(Exception):
    msg = ""


class ServiceProviderNotExist(Exception):
    msg = ""


def error_handler(e):
    response = dict()
    if isinstance(e,KeyError):
        response['error'] = str(e) + "is missing"
        response['stat'] = 400
    elif isinstance(e, DoesNotExist):
        response['error'] = "Service provider does not exist"
        response['stat'] = 400
    elif isinstance(e,ValidationError):
        response['error'] = e.message
        response['stat'] = 400
    elif isinstance(e, NotUniqueError):
        response['error'] = "Email Id already Registered"
        response['stat'] = 400
    elif isinstance(e,MethodError):
        response['error'] = e.msg
        response['stat'] = 400
    elif isinstance(e, ValueError):
        response['error'] = str(e)
        response['stat'] = 400
    elif isinstance(e, OperationError):
        response['error'] = str(e)
        response['stat'] = 400
    else:
        response['error'] = "Something went wrong"
        response['stat'] = 500
        print str(e)
        print type(e)
    return json_response(json.dumps(response), response['stat'])